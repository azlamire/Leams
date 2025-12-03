FROM node:25.2
WORKDIR /frontend
COPY package.json ./
RUN npm install 
COPY . .
EXPOSE 3000
CMD ["npm","start"]
