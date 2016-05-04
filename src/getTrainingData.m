file = fopen('../supportingFiles/newVideoLog.txt');

%I = eye(9);

tline = fgetl(file);
count = 1;
while ischar(tline)
   line = strsplit(tline, '\t');
   switch(char(line(1))) 
       case 'F'
           y(count) = 1;
           %y(count,:) = I(1,:);
           %break; 
       case 'B'
           y(count) = 2;
           %y(count,:) = I(2,:);
           %break;
       case 'R'
           y(count) = 3;
           %y(count,:) = I(3,:);
           %break;
       case 'L'
           y(count) = 4;
           %y(count,:) = I(4,:);
           %break;
       case 'FR'
           y(count) = 5;
           %y(count,:) = I(5,:);
           %break;
       case 'FL'
           y(count) = 6;
           %y(count,:) = I(6,:);
           %break;
       case 'BR'
           y(count) = 7;
           %y(count,:) = I(7,:);
           %break;
       case 'BL'
           y(count) = 8;
           %y(count,:) = I(8,:);
           %break;
       case 'N'
           y(count) = 9;
           %y(count,:) = I(9,:);
           %break;
       otherwise
           break;
   end
   frame = strsplit(char(line(2)), ' ');
   X(count, :) = cellfun(@str2num, frame);
   count = count + 1;
   tline = fgetl(file);
end

y = y';

save('NeuralNetwork/TrainingData.mat', 'X', 'y');

