var fs = require("fs");
info = fs.readFileSync("requested_data/user.info");
data = info.toString().split("\r\n");
username = data[0];
password = data[1];
shared_secret = data[2];

const request = require('request');
const cheerio = require('cheerio');
var urlStem = 'https://steamcommunity.com/market/listings/730/'; 
weaponFile = fs.readFileSync("requested_data/skinList.info").toString();
var sep = ['\r\n', ','];
weapons = weaponFile.split(new RegExp(sep.join('|'), 'g'));
var skinTypes = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred'];
// for (i = 0; i < weapons.length; i += 2) {
//     for (j = 0; j < skinTypes.length; j++) {
//         console.log(urlStem + weapons[i] + " (" + skinTypes[j] + ")");
//     }
// }


var Steam = require("steam"),
    csgo = require("csgo"),
    util = require("util"),
    Totp = require('steam-totp'),
    steamClient = new Steam.SteamClient(),
    steamUser = new Steam.SteamUser(steamClient),
    steamFriends = new Steam.SteamFriends(steamClient),
    steamGC = new Steam.SteamGameCoordinator(steamClient, 730),
    CSGOCli = new csgo.CSGOClient(steamUser, steamGC, false);
    readlineSync = require("readline-sync")
    readline = require("readline")

    var onSteamLogOn = function onSteamLogOn(response){
        if (response.eresult == Steam.EResult.OK) {
            util.log('Logged in!');
        }
        else
        {
            util.log('error, ', response);
            process.exit();
        }
        steamFriends.setPersonaState(Steam.EPersonaState.Busy);
        util.log("Logged on.");

        util.log("Current SteamID64: " + steamClient.steamID);
        util.log("Account ID: " + CSGOCli.ToAccountID(steamClient.steamID));

        CSGOCli.launch();

        CSGOCli.on("unhandled", function(message) {
            util.log("Unhandled msg");
            util.log(message);
        });

        CSGOCli.on("ready", function() {
            util.log("node-csgo ready.");
                
                console.log("collection item data");
                
                CSGOCli.itemDataRequest("0", "17842144863", "7100494772439222079", "2590076190517757054");
                
                CSGOCli.on("itemData", function(itemdata) {
                    console.log(itemdata);
                });
            });

        CSGOCli.on("unready", function onUnready(){
            util.log("node-csgo unready.");
        });

        CSGOCli.on("unhandled", function(kMsg) {
            util.log("UNHANDLED MESSAGE " + kMsg);
        });
    },
    onSteamSentry = function onSteamSentry(sentry) {
        util.log("Received sentry.");
        require('fs').writeFileSync('sentry', sentry);
    },
    onSteamServers = function onSteamServers(servers) {
        util.log("Received servers.");
        fs.writeFile('servers.json', JSON.stringify(servers, null, 2));
    }

var logOnDetails = {
    "account_name": username,
    "password": password,
    "two_factor_code": Totp.generateAuthCode(shared_secret)
};

steamClient.connect();
steamClient.on('connected', function(){
        steamUser.logOn(logOnDetails);
    });
steamClient.on("logOnResponse", onSteamLogOn);
