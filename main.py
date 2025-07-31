from Server import Server


if __name__ == "__main__":
    server = Server()
    
    print("[Main] Server is running. Type 'exit' to stop")
    
    try:
        while True:
            command = input()
            
            if command.strip().lower() == "exit":
                print("[Main] Stopping server...")
                server.shutdown()
                break
    except KeyboardInterrupt:
        print("[Main] Ctrl+C detected. Shutting down")
        server.shutdown()
        
    print("[Main] Program exited cleanly")
    