from PIL import Image
import numpy as np
import os

from numpy.typing import NDArray


class CNN_layer:
    def __init__(self,  bias: int, img: NDArray, kernel_count: int = 2) -> None:
        self.img = img
        _, _, in_ch = self.img.shape
        self.ker = np.random.randint(0,2,(3,3, in_ch ,kernel_count)).astype(np.float32)
        self.bias = np.zeros((kernel_count,), dtype=np.float32)


    def relu_derivative(self, x):
        return np.where(x > 0, 1, 0)

    def relu(self, x):
        return np.maximum(0, x)

    # ∂L/∂x = conv_full(δ_out, flip(K)) (градиент по входу conv)
    def convolution(self):
        img_h, img_w, img_ch = self.img.shape
        ker_h, ker_w, ker_ch, ker_count = self.ker.shape
        height_out = img_h - ker_h + 1
        width_out = img_w - ker_w + 1
        output = np.zeros((height_out, width_out, ker_count), dtype=np.float32)
        for count in range(ker_count):
            k = self.ker[:, :, :, count]
            b = self.bias[count]
            for h in range(height_out):
                for w in range(width_out):
                    patch = self.img[h:h + ker_h, w:w + ker_w, :]
                    output[h, w, count] = np.sum(patch * k) + b
            print("end")
        return output
        # for h in range(height_out):
        #     for w in range(width_out):
        #         height_start = h
        #         height_end = height_start + ker_h
        #         w_start = w
        #         w_end = w_start + ker_w
        #         img_patch = self.img[height_start:height_end, w_start:w_end, :]
        #         output[h, w] = np.sum(img_patch * self.ker)
        # return output

    # Pooling_size, stride
    # Backward для max‑pool — прокидываем градиент только в позиции argmax.
    def max_pooling(self, conv, pool_size=2):
        print(conv.shape)
        h, w, kernels = conv.shape

        h_out = h // pool_size
        w_out = w // pool_size
        output = np.zeros((h_out, w_out, kernels), dtype=np.float32)
        for kernel in range(kernels):
            for h in range(h_out):
                for w in range(w_out):
                    height_start = h * pool_size
                    height_end = height_start + pool_size
                    w_start = w * pool_size
                    w_end = w_start + pool_size
                    img_patch = conv[height_start:height_end, w_start:w_end]
                    output[h,w, kernel] = np.max(img_patch)
        return output

    def forward(self):
        x = self.convolution()
        x = self.relu(x)
        x = self.max_pooling(x)
        return x

    def backward(self):


def dense(x: NDArray):
    return x.flatten()

image = np.array(Image.open("./0_obnHri9w__4Cmhbj.jpg").convert('L'))
image = image[:, :, np.newaxis]
print(dense(CNN_layer(bias=1, img=image).forward()))
