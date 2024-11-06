using System;
using System.Diagnostics;
using System.Threading.Tasks;
using Agones;

class Program
{
    private static readonly AgonesSDK agonesSdk = new AgonesSDK();

    static async Task Main(string[] args)
    {

        // S'assurer que le SDK est prêt pour gérer le serveur
        await agonesSdk.ReadyAsync();

        // Lancer le serveur CS:GO
        StartCsgoServer();

        // Gérer les signaux de santé pour informer Agones que le serveur est actif
        _ = HealthCheckLoop();

        Console.WriteLine("Serveur CS:GO avec Agones est prêt. Appuyez sur Entrée pour arrêter.");
        Console.ReadLine();

        // Informer Agones que le serveur se termine
        await agonesSdk.ShutDownAsync();

    }
    public static void ProcessDirectory(string targetDirectory)
    {
        // Process the list of files found in the directory.
        string [] fileEntries = Directory.GetFiles(targetDirectory);
        foreach(string fileName in fileEntries)
            ProcessFile(fileName);

        // Recurse into subdirectories of this directory.
        string [] subdirectoryEntries = Directory.GetDirectories(targetDirectory);
        foreach(string subdirectory in subdirectoryEntries)
            ProcessDirectory(subdirectory);
    }

    // Insert logic for processing found files here.
    public static void ProcessFile(string path)
    {
        Console.WriteLine("Processed file '{0}'.", path);
    }

    private static void StartCsgoServer()
    {
        string serverPath = "/home/cs2user/cs2_server";
        ProcessDirectory(serverPath + "/game/bin/");
        var csgoProcess = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = $"{serverPath}/game/bin/win64/cs2.exe", // Assurez-vous que le chemin est correct
                Arguments = $"-dedicated -port '27015' -console -usercon +sv_setsteamaccount ECE2CDBA46245CD80E318A1449A8CBA4 +game_type 0 +game_mode 2 +map de_dust2 +sv_lan 0 +rcon_password '123456'",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true,
                WorkingDirectory = $"{serverPath}/game/bin/win64/"
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
