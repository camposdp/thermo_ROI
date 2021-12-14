%% Abrir um arquivo de imagem e recortar linhas e colunas desnecessárias
% Dr. Daniel P. Campos
% 27/07/2021
% UTFPR - AP


close all
clc
clear

nome_das_pastas = dir;
N = length(nome_das_pastas);
%pos = {'A','B'};

for i = 3:N
nome = nome_das_pastas(i).name;    
cd(nome)
%arquivos_csv=dir('*.csv');

nome_das_pastas2 = dir;
M  = length(nome_das_pastas2);

    for j = 3:M

    nome2 = nome_das_pastas2(j).name;    
    cd(nome2)
    arquivos_csv=dir('*.csv');


    if length(arquivos_csv)>0


        for j=1:length(arquivos_csv)   

            M = readmatrix(arquivos_csv(j).name,...
                 "DecimalSeparator",',');

            s = size(M);
            if s(2)==321
                M=M(:,2:end); 
            end

            csvwrite(['_' arquivos_csv(j).name],M)

        end

    end
    cd('..')

end
cd('..')
end

%%






