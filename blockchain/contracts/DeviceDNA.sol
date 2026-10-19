// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DeviceDNA {

    string private trustedDNA;

    event DNARegistered(string dna);

    function registerDNA(string memory _dna) public {
        trustedDNA = _dna;
        emit DNARegistered(_dna);
    }

    function getTrustedDNA()
        public
        view
        returns (string memory)
    {
        return trustedDNA;
    }

    function verifyDNA(string memory _currentDNA)
        public
        view
        returns (bool)
    {
        return keccak256(bytes(trustedDNA)) ==
               keccak256(bytes(_currentDNA));
    }
}
