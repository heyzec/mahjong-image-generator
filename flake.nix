{
  description = "Template for a direnv shell, with Python";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};

  in
  {
    devShells.${system}.default = pkgs.mkShell {
      buildInputs = with pkgs; [
        (let
          python-packages = ps: with ps; [
            flask
            waitress
            python-dotenv
            pillow

          ];
        in python3.withPackages python-packages)
      ];
    };
  };
}

