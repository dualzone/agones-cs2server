using System.Diagnostics;

namespace WebApplication1.ServerManager;

public class CS2Server: CS2ServerInterface

{
    
    private readonly string steamToken;
    private readonly string rconPassword;
    private readonly int gameType;
    private readonly int gameMode;
    private readonly string map;
    private readonly int serverPort;
    private readonly string launcherPath;

    private Process cs2ServerProcess;
    
    public CS2Server(
        string steamToken,
        string rconPassword,
        int gameType = 0,
        int gameMode = 2,
        string map = "dust2",
        int serverPort = 27015,
        string launcherPath = "/cs2server/game/bin/linuxsteamrt64/"
        ) 
    {
        this.steamToken = steamToken;
        this.rconPassword = rconPassword;
        this.gameType = gameType;
        this.gameMode = gameMode;
        this.map = map;
        this.serverPort = serverPort;

        var home = Environment.GetEnvironmentVariable("HOMEDIR")
                                  ?? throw new InvalidOperationException("La variable d'environnement HOMEDIR est introuvable.");
        this.launcherPath = $"{home}{launcherPath}";
        
        this.CongigureProcess();
    }

    private void CongigureProcess()
    {
        
        cs2ServerProcess = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = $"{launcherPath}/cs2",
                Arguments = $"-dedicated -port '{serverPort}' -console -usercon +sv_setsteamaccount {steamToken} +game_type {gameType} +game_mode {gameMode} +map {map} +sv_lan 0 +rcon_password '{rconPassword}'",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                RedirectStandardInput = true,
                CreateNoWindow = true,
                WorkingDirectory = launcherPath
            },
            EnableRaisingEvents = true
        };

        // Gérer les événements de sortie
        cs2ServerProcess.OutputDataReceived += (sender, e) =>
        {
            if (!string.IsNullOrEmpty(e.Data))
                Console.WriteLine($"[CS2]: {e.Data}");
        };

        cs2ServerProcess.ErrorDataReceived += (sender, e) =>
        {
            if (!string.IsNullOrEmpty(e.Data))
                Console.WriteLine($"[Erreur CS2]: {e.Data}");
        };

        // Gestion de la fin du processus
        cs2ServerProcess.Exited += (sender, e) =>
        {
            Console.WriteLine("Le processus CS2 s'est terminé.");
        };
        
    }
        
    

    public void  startServer()
    {
        Console.WriteLine("Démarrage du serveur CS2...");
        cs2ServerProcess.Start();
        cs2ServerProcess.BeginOutputReadLine();
        cs2ServerProcess.BeginErrorReadLine();
        Console.WriteLine("Le serveur CS2 est en cours d'exécution...");
    }

    public void stopServer()
    {
        if (!cs2ServerProcess.HasExited)
        {
            Console.WriteLine("Arrêt du serveur CS2...");
            cs2ServerProcess.Kill();
            cs2ServerProcess.WaitForExit();
            Console.WriteLine("Serveur CS2 arrêté.");
        }
        else
        {
            Console.WriteLine("Le serveur CS2 n'est pas en cours d'exécution.");
        }
    }

    public void sendCommand(string command)
    {
        if (!cs2ServerProcess.HasExited)
        {
            cs2ServerProcess.StandardInput.WriteLine(command);
            Console.WriteLine($"Commande envoyée : {command}");
        }
        else
        {
            Console.WriteLine("Le processus CS2 n'est pas en cours d'exécution.");
        }
    }
    
    public void WaitForServerExit()
    {
        Console.WriteLine("En attente de la fin du processus CS2...");
        cs2ServerProcess.WaitForExit();
        Console.WriteLine("Le processus CS2 s'est terminé.");
    }
}