{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    backend.url = "path:./backend";
    frontend.url = "path:./frontend";
    ansible.url = "path:./infra/ansible";
    test.url = "path:./test/";
  };

  outputs = { 
    nixpkgs,
    ansible,
    backend,
    test,
    frontend,
    ...
  }@inputs: 
    let
      forAllSystems = nixpkgs.lib.genAttrs [ "x86_64-linux" "aarch64-linux" ];
    in {
      devShells = forAllSystems (system: 
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in {
          default = pkgs.mkShell {
            # inputsFrom = map (flake: flake.devShells.${system}.default) dependencies;
            # TODO: Find the way to make it more pretty and handy PLS 
            inputsFrom = [
              backend.devShells.${system}.default
              ansible.devShells.${system}.default
              frontend.devShells.${system}.default
              test.devShells.${system}.default
            ];
            packages = with pkgs; [
              # docker for conterization and handy local/deploy usage
              docker
              # https://www.docker.com/

              # watchexec for watching the file if it's changed it used in Makefile
              watchexec
              # https://github.com/watchexec/watchexec

              # envsubst for replacing ${} env varaibles where it can't be like compose.yaml or .envs.
              # used in Makefile with watchexec
              gomplate

              # act for testing and making ci/cd. Githu actions but local
              act
              # https://github.com/nektos/act

              go-task

              cue
            ];
            env = {
              COMPOSE_FILE="./compose.letsencrypt.yaml:./compose.yaml";
            };
          };
        }
      );
    };
}

