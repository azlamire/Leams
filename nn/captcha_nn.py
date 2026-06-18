import numpy as np
from numpy.typing import NDArray
from PIL import Image
from tensorflow.keras.datasets import mnist
import time
import sys

def softmax(logits: NDArray) -> NDArray:
    e = np.exp(logits - logits.max())
    return e / e.sum()

def cross_entropy_loss_and_grad(logits: NDArray, y: int):
    probs = softmax(logits)
    loss = -np.log(probs[y] + 1e-12)
    grad = probs.copy()
    grad[y] -= 1.0
    return loss, grad

class CNN_layer:
    def __init__(self, img: NDArray, kernel_count: int = 2, kernel_size=(3,3), pool_size=2) -> None:
        self.img = img.astype(np.float32)
        kh, kw = kernel_size
        _, _, in_ch = img.shape
        self.ker = np.random.randn(kh, kw, in_ch, kernel_count).astype(np.float32) * 0.1
        self.bias = np.zeros((kernel_count,), dtype=np.float32)
        self.pool_size = pool_size
        self.z = None
        self.relu_mask = None
        self.pool_mask = None
        self.out = None
        self.dker = None
        self.db = None

    def relu(self, x):
        return np.maximum(0, x)

    def forward(self):
        img_h, img_w, img_ch = self.img.shape
        ker_h, ker_w, ker_in_ch, ker_count = self.ker.shape
        Hc = img_h - ker_h + 1
        Wc = img_w - ker_w + 1
        z = np.zeros((Hc, Wc, ker_count), dtype=np.float32)

        for oc in range(ker_count):
            k = self.ker[:, :, :, oc]
            b = self.bias[oc]
            for i in range(Hc):
                for j in range(Wc):
                    patch = self.img[i:i+ker_h, j:j+ker_w, :]
                    z[i, j, oc] = np.sum(patch * k) + b

        self.z = z
        a = self.relu(z)
        self.relu_mask = (z > 0)
        p = self.pool_size
        Hp = a.shape[0] // p
        Wp = a.shape[1] // p
        out = np.zeros((Hp, Wp, ker_count), dtype=np.float32)
        pool_mask = np.zeros_like(a, dtype=bool)

        for c in range(ker_count):
            for i in range(Hp):
                for j in range(Wp):
                    h0 = i * p
                    w0 = j * p
                    window = a[h0:h0+p, w0:w0+p, c]
                    idx = np.argmax(window)
                    r = idx // p
                    s = idx % p
                    out[i, j, c] = window[r, s]
                    pool_mask[h0 + r, w0 + s, c] = True

        self.pool_mask = pool_mask
        self.out = out
        return out

    def maxpool_backward(self, d_out: NDArray) -> NDArray:
        Hc, Wc, K = self.z.shape
        d_relu = np.zeros_like(self.z, dtype=np.float32)
        p = self.pool_size
        Hp, Wp, _ = d_out.shape

        for c in range(K):
            for i in range(Hp):
                for j in range(Wp):
                    h0 = i * p
                    w0 = j * p
                    window_mask = self.pool_mask[h0:h0+p, w0:w0+p, c]
                    if not window_mask.any():
                        continue
                    coords = np.argwhere(window_mask)[0]
                    r, s = coords
                    d_relu[h0 + r, w0 + s, c] = d_out[i, j, c]
        return d_relu

    def relu_backward(self, d_relu: NDArray) -> NDArray:
        return d_relu * self.relu_mask.astype(np.float32)

    def conv_backward(self, d_z: NDArray) -> NDArray:
        kh, kw, in_ch, K = self.ker.shape
        Hc, Wc, _ = d_z.shape
        dker = np.zeros_like(self.ker, dtype=np.float32)
        db = np.zeros_like(self.bias, dtype=np.float32)
        dimg = np.zeros_like(self.img, dtype=np.float32)
        for oc in range(K):
            for i in range(Hc):
                for j in range(Wc):
                    gz = d_z[i, j, oc]
                    if gz == 0:
                        continue
                    patch = self.img[i:i+kh, j:j+kw, :]
                    dker[:, :, :, oc] += patch * gz
                    db[oc] += gz
                    dimg[i:i+kh, j:j+kw, :] += self.ker[:, :, :, oc] * gz

        self.dker = dker
        self.db = db
        return dimg


    def backward(self, d_out: NDArray) -> NDArray:
        d_relu = self.maxpool_backward(d_out)
        d_z = self.relu_backward(d_relu)
        dimg = self.conv_backward(d_z)
        return dimg

    def step(self, lr=1e-3):
        self.ker -= lr * self.dker
        self.bias -= lr * self.db


def example_train_single_step(image_path):
    img = Image.open(image_path).convert('L').resize((32,32))
    img = np.array(img).astype(np.float32) / 255.0
    img = img[:, :, np.newaxis]

    cnn = CNN_layer(img, kernel_count=4, kernel_size=(3,3), pool_size=2)
    pooled = cnn.forward()
    feat = pooled.flatten()
    num_classes = 3
    D = feat.size
    W = np.random.randn(D, num_classes).astype(np.float32) * 0.01
    b = np.zeros((num_classes,), dtype=np.float32)
    y = 1
    logits = feat.dot(W) + b
    loss, dlogits = cross_entropy_loss_and_grad(logits, y)
    dW = np.outer(feat, dlogits)
    db = dlogits.copy()
    dfeat = dlogits.dot(W.T)
    dpool = dfeat.reshape(pooled.shape)
    dimg = cnn.backward(dpool)
    lr = 1e-2
    W -= lr * dW
    b -= lr * db
    cnn.step(lr=lr)

    return loss, W, b, cnn

def grad_check_kernel(image_path, eps=1e-4):
    img = Image.open(image_path).convert('L').resize((16,16))
    img = np.array(img).astype(np.float32) / 255.0
    img = img[:, :, np.newaxis]
    cnn = CNN_layer(img, kernel_count=2, kernel_size=(3,3), pool_size=2)
    pooled = cnn.forward()
    feat = pooled.flatten()
    num_classes = 2
    D = feat.size
    W = np.random.randn(D, num_classes).astype(np.float32) * 0.01
    b = np.zeros((num_classes,), dtype=np.float32)
    y = 0
    logits = feat.dot(W) + b
    loss, dlogits = cross_entropy_loss_and_grad(logits, y)
    dW = np.outer(feat, dlogits)
    dfeat = dlogits.dot(W.T)
    dpool = dfeat.reshape(pooled.shape)
    _ = cnn.backward(dpool)
    analytic = cnn.dker.copy()
    i,j,ic,oc = 1,1,0,0
    orig = cnn.ker[i,j,ic,oc]
    cnn.ker[i,j,ic,oc] = orig + eps
    l_plus = compute_loss_full(cnn, W, b, y)
    cnn.ker[i,j,ic,oc] = orig - eps
    l_minus = compute_loss_full(cnn, W, b, y)
    cnn.ker[i,j,ic,oc] = orig
    numerical = (l_plus - l_minus) / (2 * eps)
    return analytic[i,j,ic,oc], numerical

def compute_loss_full(cnn_obj, W, b, y):
    pooled = cnn_obj.forward()
    feat = pooled.flatten()
    logits = feat.dot(W) + b
    loss, _ = cross_entropy_loss_and_grad(logits, y)
    return loss
def predict_image(image_path: str, cnn_obj, W: NDArray, b: NDArray, resize=(32,32)):
    img = Image.open(image_path).convert('L').resize(resize)
    x = np.array(img).astype(np.float32) / 255.0
    x = x[:, :, np.newaxis]

    cnn_obj.img = x
    pooled = cnn_obj.forward()
    feat = pooled.flatten()
    logits = feat.dot(W) + b
    probs = softmax(logits)
    pred = int(np.argmax(probs))
    return pred, probs

if __name__ == "__main__":
    epochs = 3
    lr = 1e-2
    train_subset = 5000
    resize_to = (32, 32)
    num_classes = 10
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    X_train = X_train.astype(np.float32) / 255.0
    X_test  = X_test.astype(np.float32) / 255.0

    if train_subset is not None:
        X_train = X_train[:train_subset]
        y_train = y_train[:train_subset]
    def resize_img_arr(arr, size):
        img = Image.fromarray((arr * 255).astype(np.uint8))
        img = img.resize(size, Image.BILINEAR)
        a = np.array(img).astype(np.float32) / 255.0
        return a
    example_img = resize_img_arr(X_train[0], resize_to)
    example_img = example_img[:, :, np.newaxis]
    cnn = CNN_layer(example_img, kernel_count=8, kernel_size=(3,3), pool_size=2)
    pooled = cnn.forward()
    D = pooled.flatten().size
    W = np.random.randn(D, num_classes).astype(np.float32) * 0.01
    b = np.zeros((num_classes,), dtype=np.float32)
    N = X_train.shape[0]
    print("Train samples:", N, "feature dim D =", D)
    for epoch in range(1, epochs+1):
        t0 = time.time()

        perm = np.random.permutation(N)
        total_loss = 0.0
        correct = 0
        for idx in range(N):
            i = perm[idx]
            img_res = resize_img_arr(X_train[i], resize_to)
            img_res = img_res[:, :, np.newaxis]
            y = int(y_train[i])
            cnn.img = img_res
            pooled = cnn.forward()
            feat = pooled.flatten()
            logits = feat.dot(W) + b
            loss, dlogits = cross_entropy_loss_and_grad(logits, y)
            total_loss += float(loss)
            dW = np.outer(feat, dlogits)
            db = dlogits.copy()
            dfeat = dlogits.dot(W.T)
            dpool = dfeat.reshape(pooled.shape)
            _ = cnn.backward(dpool)
            W -= lr * dW
            b -= lr * db
            cnn.step(lr=lr)
            pred = int(np.argmax(softmax(logits)))
            if pred == y:
                correct += 1
            if (idx + 1) % 1000 == 0:
                print(f"Epoch {epoch} step {idx+1}/{N} ...")

        avg_loss = total_loss / N
        acc = correct / N
        print(f"Epoch {epoch}/{epochs} time={(time.time()-t0):.1f}s loss={avg_loss:.4f} acc={acc:.4f}")


    M = 500
    correct = 0
    for i in range(M):
        img_res = resize_img_arr(X_test[i], resize_to)[:, :, np.newaxis]
        cnn.img = img_res
        pooled = cnn.forward()
        feat = pooled.flatten()
        logits = feat.dot(W) + b
        pred = int(np.argmax(softmax(logits)))
        if pred == int(y_test[i]):
            correct += 1
    img_path = "./3.jpg"
    pred, probs = predict_image(img_path, cnn, W, b, resize=resize_to)
    print("Predicted class for", img_path, ":", pred)
    print("Probs:", np.round(probs, 4))
