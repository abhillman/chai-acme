{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell rec {
  # Add packages by referencing https://search.nixos.org/
  buildInputs = with pkgs;[
      black # python code formatter
      python311
      python311Packages.lxml
  ];
}
