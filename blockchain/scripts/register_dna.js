const fs = require("fs");
const path = require("path");

const DeviceDNA = artifacts.require("DeviceDNA");

module.exports = async function(callback) {

    try {

        const contract = await DeviceDNA.deployed();

        const dnaFile = path.join(
            __dirname,
            "../../baseline/baseline_hash.txt"
        );

        const trustedDNA = fs
            .readFileSync(dnaFile, "utf8")
            .trim();

        await contract.registerDNA(trustedDNA);

        const storedDNA =
            await contract.getTrustedDNA();

        console.log("");
        console.log("====================================");
        console.log("CYBERSCOPE TRUSTED DNA REGISTERED");
        console.log("====================================");
        console.log("");

        console.log("Contract Address:");
        console.log(contract.address);

        console.log("");

        console.log("Trusted DNA:");
        console.log(storedDNA);

        console.log("");
        console.log("====================================");

        callback();

    } catch (error) {

        console.error(error);
        callback(error);

    }

};
