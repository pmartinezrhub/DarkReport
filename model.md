What we need?

- Projects - cause you will do project, no matter the client.

Each project can have a number of reports


- Reports - 

Each report can have a number of findings

Machine - Target - Url - Domain, etc.


- Findings - 


- 🔎 [Reconnaissance] -- A space to show how reconnissance was done. Like , Wappalizzer, nmap ,etc. 
                         Why is optional, cause you dont need to explain how you find obviulsy things.   

- 🔪 [Weaponization]  -- Create a payload or search for one CVE etc, that can work with the target
                          Why is this optional. cause sometimes is implicit you need a weapon to next stage
                          May be as part of report we can show it as a CVE list if it exists.  

- 🎯 📨 Delivery       -- The method to delivery payload , email, form, POST, malicious link, infected USB, watering-hole attack

- 🪲 Explotation    -- CVE itself, How the payload works - Sometimes we dont know how the exploit works, just a shellcode

- 🎁 [Installation]   --  Explanation FLI  (e.g., rootkits, Trojans, backdoors, webshell).
                          Why is this optional cause sometimes you dont need to make an instalation to obtain RCE. In terms of pentestings is should be done to escalate privileges, but not always mandatory. 

- 🎮 [Command & Control C2] --  Explanation of how you can perform things than you should not. 
                                Why is this optional, cause you dont need to explain how to take remote control.
                                also you should install a RAT or similar tool for showing up to client.  
                                You will explain in next stage.  


- 😈 Actions on Objectives -- Explanation of what can do the attacker once it takes control, like, data theft,
                           ransomware deployment, sabotage, espionage, or disruption 


Basically findings are targered to find how the attack can be exploited and what can do the postexplotation. 
I mean you can explain a client, ok the attacker can install a RAT and steal the information, but you dont need to explain how a RAT works.

In short, is basically to how the attack is performed (delivery), a short explanation of hwo the attack works (explotation), and what actions can the attackers perform applying this (actions). 