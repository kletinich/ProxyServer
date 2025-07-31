# ProxyServer
A simple Proxy Server project. For now the project supports only http requests. Any other protocol will return 501 code.

# How to run:
## Step 1: Start the Proxy Server
  1. Run the server.
## Step 2: Configure your browser to use the proxy
  1. Open your browser's proxy settings.
  2. Set the following:
     * HTTP Proxy: 127.0.0.1
     * Port: 12345
     * Https Proxy: You can enable it, but a 501 error message will be displayed.
  3. Save the settings.
## Step 3: Test with a HTTP Websites
  1. Open a site that uses HTTP.
  2. URL For a site: [testingmcafeesites](http://www.testingmcafeesites.com/)
## Step 4: Stop the server
  1. Press 'exit' or CTRL + C in the terminal to stop the Proxy Server.
  2. Disable the proxy configurations in your browser.
