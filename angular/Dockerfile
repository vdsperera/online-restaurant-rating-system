### Stage 01: build ###

FROM mhart/alpine-node:12 as builder

# Set working directory
RUN mkdir  /app
WORKDIR /app

# Copy app dependencies
COPY restaurant-rating-system/package.json restaurant-rating-system/package-lock.json /app/restaurant-rating-system/


# Install app dependencies
RUN npm install --prefix restaurant-rating-system

# Copy app files
COPY . /app

# Build app
RUN npm run build --prefix restaurant-rating-system -- --output-path=./dist/out


### Stage 02: delivery ###

FROM nginx:1.15.7-alpine:stable

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy output directory from builder to nginx image.
COPY --from=builder /app/restaurant-rating-system/dist/out /usr/share/nginx/html

# Copy nginx configuration file.
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf