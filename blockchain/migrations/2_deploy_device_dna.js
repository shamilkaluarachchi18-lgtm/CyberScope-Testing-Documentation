const DeviceDNA = artifacts.require("DeviceDNA");

module.exports = function (deployer) {
    deployer.deploy(DeviceDNA);
};
