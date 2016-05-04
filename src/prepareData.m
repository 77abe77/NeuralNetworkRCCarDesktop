fid = fopen('../supportingFiles/myFile.txt', 'w+');

fprintf(fid, 'S\n');
for i=1:size(Theta1, 1)
    fprintf(fid, '%f ', Theta1(i,:));
    fprintf(fid, '\n');
end
%fprintf(fid, '%f', Theta1((i + 1),:));
%fprintf(fid, '\n');
fprintf(fid, '!');

for i=1:size(Theta2, 1)
    fprintf(fid, '%f ', Theta2(i,:));
    fprintf(fid, '\n');
end
%fprintf(fid, '%f', Theta2((i + 1),:));
%fprintf(fid, '\n');
fprintf(fid, 'E');