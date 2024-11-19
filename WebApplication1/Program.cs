using System.Diagnostics;
using Agones;
using WebApplication1.ServerManager;

namespace WebApplication1;

class Program
{
    private static readonly AgonesSDK agonesSdk = new AgonesSDK();

    static async Task Main(string[] args)
    {

        // S'assurer que le SDK est prêt pour gérer le serveur
        await agonesSdk.ReadyAsync();
        
        var steamToken = Environment.GetEnvironmentVariable("CS2_STEAM_TOKEN")
                          ?? throw new InvalidOperationException("La variable d'environnement CS2_STEAM_TOKEN est introuvable.");
        
        var rconPassword = Environment.GetEnvironmentVariable("CS2_RCON_PASSWORD")
                            ?? throw new InvalidOperationException("La variable d'environnement CS2_RCON_PASSWORD est introuvable.");

        // Lancer le serveur CS:GO
        var server = new CS2Server(
            steamToken: steamToken,
            rconPassword: rconPassword
        );
        
        server.startServer();
        
        server.WaitForServerExit();
        _ = HealthCheckLoop();

        // Informer Agones que le serveur se termine
        await agonesSdk.ShutDownAsync();

    }
    

    private static async Task HealthCheckLoop()
    {
        while (true)
        {
            await agonesSdk.HealthAsync();
            Console.WriteLine($"[HEALTH] send health ping");
            await Task.Delay(10000); // Envoie un signal de santé toutes les 10 secondes
        }
    }
}