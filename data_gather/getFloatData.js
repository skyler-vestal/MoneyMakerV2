var fs = require("fs");
info = fs.readFileSync("requested_data/user.info");
data = info.toString().split("\r\n");
username = data[0];
password = data[1];
shared_secret = data[2];

db_path = "F:/Dev/py-workspace/SkinDatabase/skins.db"

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

const sqlite3 = require('sqlite3');
let db = new sqlite3.Database(db_path, sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
        return console.error(err.message);
    }
    console.log('Connected to skin database.');
    });
db.configure("busyTimeout", 10000);

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
                updateFloats();

                CSGOCli.on("itemData", function(itemdata) {
                    itemIDData = itemdata.iteminfo.itemid;
                    itemID = getIDArr(+itemIDData.low, +itemIDData.high);
                    floatID = itemdata.iteminfo.floatvalue;
                    data = [floatID.toString(), itemID.toString()];
                    db.run(`UPDATE skins SET float = ? WHERE asset_id = ?`, data, function(err) {
                        if (err) {
                            console.log(err.message);
                        } else {
                            console.log("ItemID: " + itemID + " | Float: " + floatID);
                        }
                    });
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

function updateFloats() {
    db.all("SELECT * FROM skins WHERE float=0", [], (err, result) => {
        if (err) {
            console.log(err);
        } else {
            result.forEach((skin, index) => {
                setTimeout(function() {
                    CSGOCli.itemDataRequest("0", skin.asset_id, skin.dick_id, skin.market_id);
                    console.log(`Item request: A:${skin.asset_id} D:${skin.dick_id} M:${skin.market_id}`);}, 
                        1100 * (index + 1));
            });
        }
    });
}

function getIDArr(lowInt, highInt) {
    numList = []
    for (i = 0; i <= 7; i++) {
        shift = i * 8
        if (i <= 3) {
            numList[i] = (lowInt & (0xFF << shift)) >> shift;
        } else {
            numList[i] = (highInt & (0xFF << shift)) >> shift;
        }
    }
    buf = Buffer.from(numList);
    return buf.readBigUInt64LE(0);
}

var stdin = process.stdin;
stdin.setRawMode( true );
stdin.resume();
stdin.setEncoding( 'utf8' );

stdin.on('data', function(key){
  if (key === '\u0003') {
    console.log("Closing down database and bot.");
    steamClient.disconnect();
    db.close();
    process.exit();
  }
});

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
