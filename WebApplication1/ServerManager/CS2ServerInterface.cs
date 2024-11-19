using System.Diagnostics;

namespace WebApplication1.ServerManager;

public interface CS2ServerInterface
{
    
    public void startServer();
    
    public void stopServer();
    
    public void sendCommand(string command);
    
}