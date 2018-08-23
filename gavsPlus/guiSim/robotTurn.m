function play = robotTurn(hObject, eventdata, handles)
% Function to implement computer skill and have it play

global states
global game

rLoc = find(ismember(states, 'robot'));
hLoc = find(ismember(states, 'human'));
if hLoc<= 3; goal=1; else goal=2; end;
rLoc = [floor(rLoc/3.1) rLoc-3*floor(rLoc/3.1)-1];
hLoc = [floor(hLoc/3.1) hLoc-3*floor(hLoc/3.1)-1];

state = goal + rLoc(2)*2 + rLoc(1)*3*2 + hLoc(2)*2*3*2 + hLoc(1)*3*2*3*2 -1;


if game==1
    dec = [4 2;53 2;39 1;22 5;47 5;63 1;69 5;49 4;8 2;67 4;32 2;37 1;18 1;24 1;12 1;30 1;55 4;6 4;61 1];
elseif game==2
    % H-K init 2
    dec = [41 6;16 6;59 3;65 2;10 5;34 5;69 4;20 4;2 5;51 1;37 1;61 1;12 4;24 4;49 4;55 4;30 4;6 4;18 4;67 4;63 5];
end

ind = dec(:,1)==state;
play = dec(ind,2);

