function result = checkWin(hObject, eventdata, handles)
% Function to check if game is over

global states;

rLoc = find(ismember(states, 'robot'));
hLoc = find(ismember(states, 'human'));

result = 0;
if hLoc==6 && (rLoc==1 || rLoc==4)
    set(handles.edit2, 'string', 'Win')
    result = 1;
end


