{
  description = "Devshell";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }: let
    forAllSystems = function:
      nixpkgs.lib.genAttrs [
        "x86_64-linux"
        "aarch64-linux"
      ] (system: function nixpkgs.legacyPackages.${system});
  in {
    devShells = forAllSystems (pkgs: {
      default = pkgs.mkShellNoCC {
        buildInputs = with pkgs; [
          (python3.withPackages (p: with p; [
            fastapi 
            pydantic
            pytest
            pytest-asyncio
            fastapi-cli
            httpx
            jinja2
            python-multipart
            email-validator
            uvicorn
          ]))
        ];
      };
    });
  };
}

