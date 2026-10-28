function sfdr_plotspec(caseDir, toolboxSrc)
%SFDR_PLOTSPEC MATLAB ADCToolbox plotspec on the SFDR cases of issue #36 (docs/sfdr-estimator.md).
%   python tests/sfdr_cases.py <caseDir>
%   matlab -batch "addpath('tests/matlab'); sfdr_plotspec('<caseDir>', '<ADCToolbox>/matlab/src')"
%   writes <caseDir>/matlab_plotspec.csv: case, SFDR, SNDR, THD (dB). The expected SFDR values
%   are MATLAB_PLOTSPEC in tests/sfdr_cases.py.
addpath(genpath(toolboxSrc));
d = dir(fullfile(caseDir, '*.txt'));
fid = fopen(fullfile(caseDir, 'matlab_plotspec.csv'), 'w');
fprintf(fid, 'case,sfdr,sndr,thd\n');
warning('off', 'all');
for i = 1:numel(d)
    x = load(fullfile(d(i).folder, d(i).name));
    [~, sndr, sfdr, ~, thd] = plotspec(x(:)', 100e6, 2, 5, 'disp', false);
    [~, name] = fileparts(d(i).name);
    fprintf(fid, '%s,%.10g,%.10g,%.10g\n', name, sfdr, sndr, thd);
end
fclose(fid);
end
