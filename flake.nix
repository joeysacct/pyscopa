{
    description = "basic python dev env";

    inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
    };

    outputs = {self, nixpkgs, }:
        let
            system = "x86_64-linux";
            pkgs = import nixpkgs {inherit system;};

        in {
            devShells.${system}.default =
                pkgs.mkShell {
                    packages = with pkgs; [
                        (python312.withPackages (ps: with ps; [
                            numpy
                            matplotlib
                            scipy
                            beautifulsoup4
                            pandas
                            requests
                            lxml
                        ]))
                    ];
                };
        };
}
