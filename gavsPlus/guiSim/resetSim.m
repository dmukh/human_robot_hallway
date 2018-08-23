function resetSim(hObject, eventdata, handles)
% Reset grid for new simulation

global states;
global ended;
global game;

% Loop to clear push button content
for k = 1:6   
    set(eval(['handles.pushbutton' num2str(k)]), 'string','')
end

% Reset to initial conditions
if game == 1
    set(handles.pushbutton4, 'string', 'Human', 'ForegroundColor', [0 0 1]);
    set(handles.pushbutton3, 'string', 'Robot', 'ForegroundColor', [0 1 0]);
    set(handles.edit1, 'string', 'Goal: 2');
    set(handles.edit2, 'string', 'Human Move');
    ended = 0;
    states = {'0';'0';'robot';'human';'0';'0'};
elseif game == 2
    set(handles.pushbutton1, 'string', 'Human', 'ForegroundColor', [0 0 1]);
    set(handles.pushbutton3, 'string', 'Robot', 'ForegroundColor', [0 1 0]);
    set(handles.edit1, 'string', 'Goal: 1');
    set(handles.edit2, 'string', 'Human Move');
    ended = 0;
    states = {'human';'0';'robot';'0';'0';'0'};
end