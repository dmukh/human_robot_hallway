function processHumanMove(hObject, eventdata, handles, choice)

global states;
global ended;

if (~ismember(states{choice}, '0'))                         % check if chosen box is free
    set(handles.edit2,'string','Invalid')
    return                                          
end


% Insert 'Human' into chosen box and clear old box
set(eval(['handles.pushbutton' num2str(choice)]),'string','Human','ForegroundColor',[0 0 1])
oldHuman = find(ismember(states,'human'));
set(eval(['handles.pushbutton' num2str(oldHuman)]),'string','')
states{oldHuman} = '0';
states{choice} = 'human';

% Update goal
if choice <= 3
    set(handles.edit1, 'string', 'Goal: 1')
else
    set(handles.edit1, 'string', 'Goal: 2')
end

ended = checkWin(hObject, eventdata, handles);
if ended ~= 0
    return
end

pause(.2)


loop = 1;
while ~ended && loop==1
    % Call computer's turn; place robot on push button
    oldRobot = find(ismember(states,'robot'));
    set(eval(['handles.pushbutton' num2str(oldRobot)]),'string','')
    tmp = robotTurn(hObject, eventdata, handles);
    set(eval(['handles.pushbutton' num2str(tmp)]), 'string','Robot','ForegroundColor',[0 1 0])
    
    states{oldRobot} = '0';
    states{tmp} = 'robot';
    
    set(handles.edit2,'string','Robot Move')
    
    % Check if that play won the match
    ended = checkWin(hObject, eventdata, handles);
    if ended ~= 0
        return
    end
    
    if states{6} == 'human'
        loop=1;
        pause(.5)
    else
        loop=0;
    end
end

