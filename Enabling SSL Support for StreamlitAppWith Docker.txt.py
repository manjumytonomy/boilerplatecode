Here are the steps to enable HTTPS support with a self-signed CA certificate for your Streamlit app:


Step 1: Generate self-signed CA certificate

Create a self-signed CA certificate using OpenSSL:



bash
openssl req -x509 -newkey rsa:2048 -nodes -keyout streamlit.key -out streamlit.crt -days 365 -subj "/C=US/ST=State/L=Locality/O=Organization/CN=localhost"


This command generates:


- streamlit.key (private key)
- streamlit.crt (self-signed certificate)


Step 2: Update Dockerfile

Update your Dockerfile to copy the certificate and key:



# ...

# Copy certificate and key
COPY streamlit.crt /etc/ssl/certs/
COPY streamlit.key /etc/ssl/private/

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app on container startup with HTTPS
CMD ["streamlit", "run", "--server.ssl-cert-file", "/etc/ssl/certs/streamlit.crt", "--server.ssl-key-file", "/etc/ssl/private/streamlit.key", "app.py"]



Step 3: Update docker run command

Update your docker run command to map the certificate and key:



bash
docker run -p 8501:8501 -v $(pwd)/streamlit.crt:/etc/ssl/certs/streamlit.crt -v $(pwd)/streamlit.key:/etc/ssl/private/streamlit.key my-streamlit-app



Alternatively, you can bake the certificate and key into the Docker image:



# ...

# Copy certificate and key
COPY streamlit.crt /etc/ssl/certs/
COPY streamlit.key /etc/ssl/private/



Step 4: Access Streamlit app over HTTPS

Access your Streamlit app at https://localhost:8501.


Important Notes:


- Self-signed certificates will trigger browser warnings.
- For production environments, consider obtaining a trusted CA certificate.
- Ensure the certificate and key are securely stored and managed.


Additional Options:


- To specify a custom SSL port, use --server.port option.
- To disable HTTP access, use --server.enable-https and --server.disable-http options.


By following these steps, you'll enable HTTPS support for your Streamlit app using a self-signed CA certificate.