# Dockerfile for Lambda deployment package
# This creates a Lambda-compatible deployment package with all dependencies

FROM public.ecr.aws/lambda/python:3.11

# Set working directory
WORKDIR /var/task

# Copy requirements
COPY requirements.txt .
COPY layer_requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt -t .
RUN pip install --no-cache-dir -r layer_requirements.txt -t .

# Copy Lambda functions
COPY lambda_functions/ ./lambda_functions/

# Copy shared modules
COPY shared/ ./shared/

# Set Lambda handler
CMD ["lambda_functions.voice_transcribe.lambda_handler"]
