FROM node:alpine as build
COPY vue /app
WORKDIR /app
RUN yarn build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
