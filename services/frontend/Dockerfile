# Use an official Node.js image as the base image
FROM node:16-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package*.json ./

# Install dependencies
RUN npm install --silent

# Copy the rest of the app's source code into the container
COPY . .

# Expose port 3000 for the React app
EXPOSE 3000

# Start the React app (in development mode)
CMD ["npm", "start"]
