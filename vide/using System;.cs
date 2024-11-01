using System;
using System.Diagnostics;
using System.Threading.Tasks;
using Agones;

class Program
{
    private static readonly AgonesSDK agonesSdk = new AgonesSDK();

    static async Task Main(string[] args)
    {
        // Initialiser Agones
        await agonesSdk.ConnectAsync();

        // S'assurer que le SDK est prêt pour gérer le serveur
        await agonesSdk.ReadyAsync();

        // Lancer le serveur CS:GO
        StartCsgoServer();

        // Gérer les signaux de santé pour informer Agones que le serveur est actif
        _ = HealthCheckLoop();

        Console.WriteLine("Serveur CS:GO avec Agones est prêt. Appuyez sur Entrée pour arrêter.");
        Console.ReadLine();

        // Informer Agones que le serveur se termine
        await agonesSdk.ShutdownAsync();
    }

    private static void StartCsgoServer()
    {
        var steamToken = "ECE2CDBA46245CD80E318A1449A8CBA4"; // Remplacez par votre token Steam

        var csgoProcess = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = "srcds_run", // Assurez-vous que le chemin est correct
                Arguments = $"-game csgo -console -usercon +game_type 0 +game_mode 1 +map de_dust2 +sv_setsteamaccount {steamToken} -port 27015",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            }
        };

        csgoProcess.OutputDataReceived += (sender, e) => Console.WriteLine(e.Data);
        csgoProcess.ErrorDataReceived += (sender, e) => Console.WriteLine("Erreur : " + e.Data);

        csgoProcess.Start();
        csgoProcess.BeginOutputReadLine();
        csgoProcess.BeginErrorReadLine();
    }

    private static async Task HealthCheckLoop()
    {
        while (true)
        {
            await agonesSdk.HealthAsync();
            await Task.Delay(10000); // Envoie un signal de santé toutes les 10 secondes
        }
    }
}
