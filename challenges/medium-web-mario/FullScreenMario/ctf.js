/* ctf.js */
// Everything specific to the CTF challenge lives here so the original engine
// files stay (almost) untouched. Loaded after the engine scripts.
//
// The secret chamber is only reachable through the /Xampl3/ directory,
// which sets window.CTF_SECRET = true before the engine boots (see mario.js).

/* ----------------------------------------------------------------------------
 * The hidden chamber.
 *
 * The player drops into a sealed Stone box that fills the whole screen: floor,
 * ceiling and two walls at the very edges, no exit and no enemies. The camera
 * is locked (no scrolling) so nothing is ever cut off. Somewhere inside, at one
 * exact column, a single invisible Block is waiting. Jump and bump it from
 * below and the flag appears.
 *
 * The play area is 160 spaces wide (a 640px / unitsize-4 viewport), so the walls
 * sit at x=0 and x=152 to seal both edges.
 * -------------------------------------------------------------------------- */
function WorldSecret(map) {
  // No time pressure inside the puzzle room.
  map.time = Infinity;

  // Lock the camera: entrySecret runs AFTER setAreaPostCreation (which would
  // otherwise reset canscroll back to true), so we disable scrolling there.
  map.locs = [ new Location(0, entrySecret) ];

  map.areas = [
    new Area("Underworld", function() {
      setLocationGeneration(0);

      // --- The box (fills the framed viewport) ---------------------------
      pushPreFloor(0, 0, 20);                 // full-width floor  (x 0..160)
      pushPreThing(Stone, 0,   88, 1, 11);    // left wall  (x 0..8)
      pushPreThing(Stone, 152, 88, 1, 11);    // right wall (x 152..160)
      pushPreThing(Stone, 0, 96, 20, 1);      // ceiling slab across the top

      // --- The hidden flag block ----------------------------------------
      // Invisible Block sitting at one exact column near the middle. Hitting it
      // from below reveals the flag. We replace its bump handler so it shows the
      // flag instead of spawning a coin.
      var block = pushPreThing(Block, 80, jumplev1, false, true).object;
      block.bottomBump = flagBlockBump;
      block.contents = [Coin, false, false]; // harmless fallback

      // --- Ambience / taunt ---------------------------------------------
      var note = "";
      note += "<div style='color:#fff;text-align:center;font-size:12px;";
      note += "line-height:200%;text-shadow:2px 2px #000;'>";
      note += "YOU SHOULDN'T BE HERE...<br>";
      note += "BUT SINCE YOU ARE -<br>";
      note += "THE WAY OUT IS RIGHT ABOVE YOU.<br>";
      note += "JUMP IN THE RIGHT SPOT.";
      note += "</div>";
      pushPreText({ innerHTML: note }, 36, 70);
    })
  ];
}

// Entry for the chamber: place the player normally, then lock the camera.
function entrySecret(me) {
  entryPlain(me);
  map.canscroll = false;
}

/* ----------------------------------------------------------------------------
 * Custom bump handler for the hidden flag block.
 * Mirrors blockBump() but, instead of releasing contents, fetches and shows
 * the flag.
 * -------------------------------------------------------------------------- */
function flagBlockBump(me, character) {
  if(character.type != "player") return;
  if(me.used) {
    AudioPlayer.play("Bump");
    return;
  }
  me.used = 1;
  me.hidden = me.skipoverlaps = false;
  me.up = character;
  blockBumpMovement(me);
  removeClass(me, "hidden");
  switchClass(me, "unused", "used");
  AudioPlayer.play("Powerup Appears");

  ctfRevealFlag();
}

/* ----------------------------------------------------------------------------
 * Handshake step 1: arm the session as soon as the secret level loads.
 * Stores the per-session challenge token for the flag request later.
 * -------------------------------------------------------------------------- */
function ctfArm() {
  var url = window.CTF_ARM_URL || "arm.php",
      xhr = new XMLHttpRequest();
  xhr.open("POST", url, true);
  xhr.onreadystatechange = function() {
    if(xhr.readyState != 4) return;
    try { window.ctf_token = JSON.parse(xhr.responseText).token; } catch(e) {}
  };
  xhr.send();
}

/* ----------------------------------------------------------------------------
 * Handshake step 2: ask the server for this session's flag and show it.
 * POSTs the challenge token; the server only answers an armed session.
 * -------------------------------------------------------------------------- */
function ctfRevealFlag() {
  if(window.ctf_flag_shown) return;
  window.ctf_flag_shown = true;

  var url = window.CTF_FLAG_URL || "flag.php",
      xhr = new XMLHttpRequest();

  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.onreadystatechange = function() {
    if(xhr.readyState != 4) return;
    if(xhr.status == 200 && xhr.responseText) {
      ctfShowOverlay(xhr.responseText.replace(/^\s+|\s+$/g, ""));
    } else {
      ctfShowOverlay("HL4{...}", "Couldn't validate. Reload the level and try again.");
    }
  };
  xhr.onerror = function() {
    ctfShowOverlay("HL4{...}", "Flag service unreachable.");
  };
  xhr.send("token=" + encodeURIComponent(window.ctf_token || ""));
}

/* ----------------------------------------------------------------------------
 * The win overlay. Freezes the game and prints the flag.
 * -------------------------------------------------------------------------- */
function ctfShowOverlay(flag, errnote) {
  if(typeof pause == "function") try { pause(); } catch(e) {}

  var box = document.createElement("div");
  box.id = "ctf-flag-overlay";
  box.style.cssText = [
    "position:fixed", "top:0", "left:0", "right:0", "bottom:0",
    "z-index:99999", "display:flex", "flex-direction:column",
    "align-items:center", "justify-content:center", "text-align:center",
    "background:rgba(0,0,0,0.88)", "color:#fff",
    "font-family:'Press Start', monospace", "padding:20px"
  ].join(";");

  var footer = errnote
    ? "<div style='margin-top:22px;font-size:9px;color:#ff6b6b;line-height:180%;'>" +
        flagEscape(errnote) + "</div>"
    : "<div style='margin-top:22px;font-size:9px;color:#888;line-height:180%;'>" +
        "THIS FLAG IS UNIQUE TO YOUR SESSION.<br>SUBMIT IT TO SCORE.</div>";

  box.innerHTML =
    "<div style='color:#fbd000;font-size:20px;text-shadow:3px 3px #000;'>SECRET BLOCK FOUND!</div>" +
    "<div style='margin-top:24px;font-size:11px;color:#9fd0ff;'>YOUR FLAG:</div>" +
    "<div style='margin-top:12px;padding:14px 18px;background:#111;border:3px solid #fbd000;" +
    "border-radius:6px;color:#7CFC00;font-size:14px;word-break:break-all;max-width:90%;'>" +
    flagEscape(flag) + "</div>" +
    footer;

  document.body.appendChild(box);
}

/* Fire the handshake's arm step as soon as this script loads in the secret level. */
if(window.CTF_SECRET) {
  ctfArm();
}

// Tiny HTML escaper so a flag can't inject markup into the overlay.
function flagEscape(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}
