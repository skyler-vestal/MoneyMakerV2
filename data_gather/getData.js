var Steam = require('steam'),
    steamClient = new Steam.SteamClient(),
    steamUser = new Steam.SteamUser(steamClient),
    steamGC = new Steam.SteamGameCoordinator(steamClient, 730),
    csgo = require('csgo'),
    CSGO = new csgo.CSGOClient(steamUser, steamGC, false);
   
steamClient.connect();
steamClient.on('connected', function() {
    steamUser.logOn({
    account_name: 'username',
    password: 'password'
    });
});
