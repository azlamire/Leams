{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { nixpkgs, ... }: 
    let
      forAllSystems = nixpkgs.lib. genAttrs [ "x86_64-linux" "aarch64-linux" ];
    in {
      devShells = forAllSystems (system: 
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in {
          default = pkgs.mkShell {
            packages = with nixpkgs.legacyPackages.${system}; [
              uv 
              protonmail-bridge
              cloudflare-cli
            ];
            shellHook = ''
              source .venv/bin/activate
              uv add .
            '';
         };
        }
      );
    };
}

