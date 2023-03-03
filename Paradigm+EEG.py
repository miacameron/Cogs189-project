import psychopy.visual
import psychopy.event
import time
import numpy as np 
import pylsl
import random

#Global variables
#win = None
mrksream_out = None
results_in = None
fixation = None
bg_color = [0,0,0]
win_w = 800 
win_h = 600
refresh_rate = 165

win = psychopy.visual.Window(
        screen = 0,
        size=[win_w, win_h],
        units="pix",
        fullscr=False,
        color=bg_color,
        gammaErrorPolicy = "ignore"
    )

########################## Task Paradigm #####################################
def Paradigm (num_trials = 1): #constructing what our session will look like 
    terminate = False
    
    #Instructions for entire task 
    intro_text = psychopy.visual.TextStim(win,
                    'Insert Instructions here', font='Open Sans', units='pix', 
                    pos=(0,0), alignText='center',
                    height=36, color=[1, 1, 1]
                    )
                    
    #Instruct to relax while staring at the screen
    relax_text1 = psychopy.visual.TextStim(win,
                    'Relax and stare blankly at the screen', font='Open Sans', units='pix', 
                    pos=(0,0), alignText='center',
                    height=36, color=[1, 1, 1]
                    )
                    
    #Instruct to relax while closing your eyes
    relax_text2 = psychopy.visual.TextStim(win,
                    'Relax and close your eyes', font='Open Sans', units='pix', 
                    pos=(0,0), alignText='center',
                    height=36, color=[1, 1, 1]
                    )
    
    #Instruct to solve problem
    thinking_text = psychopy.visual.TextStim(win,
                    'Solve this problem mentally', font='Open Sans', units='pix', 
                    pos=(0,0), alignText='center',
                    height=36, color=[1, 1, 1]
                    )
                    
    #Problem to solve
    problem_text = psychopy.visual.TextStim(win,
                    'Insert problem to solve here', font='Open Sans', units='pix', 
                    pos=(0,0), alignText='center',
                    height=36, color=[1, 1, 1]
                    )
                    
    for i in range(num_trials):
        
        # 2000 ms overall instructions
        for frame in range(MsToFrames(2000, refresh_rate)):
            intro_text.draw()
            win.flip()
            
        # 2000ms prompt to start relaxing
        for frame in range(MsToFrames(2000, refresh_rate)):
            relax_text1.draw()
            win.flip()
            
        # 3000ms blank screen (send LSL marker here)
        for frame in range(MsToFrames(3000, refresh_rate)):
            # Send LSL marker on first frame
            if frame == 0:
                mrkstream_out.push_sample(pylsl.vectorstr([trial]))
            win.flip()
            
        # 2000ms prompt to start problem solving task
        for frame in range(MsToFrames(2000, refresh_rate)):
            thinking_text.draw()
            win.flip()
        
        # 3000ms blank screen (send LSL marker here)
        for frame in range(MsToFrames(3000, refresh_rate)):
            # Send LSL marker on first frame
            if frame == 0:
                mrkstream_out.push_sample(pylsl.vectorstr([trial]))
            problem_text.draw()
            win.flip()
            
        # 2000ms prompt to start relaxing again with eyes closed
        for frame in range(MsToFrames(2000, refresh_rate)):
            relax_text2.draw()
            win.flip()
        #######################End of Paradigm? #############################  
        '''# Flip screen and send blank
        win.flip()
        mrkstream_out.push_sample(pylsl.vectorstr(['blank']))
       
        # Wait until we get a valid result from the backend
        results = None
        print('Looking for result')
        while results is None and terminate == False:
            results, t = results_in.pull_sample(timeout=0)  
            if terminate:
                break
        
        # Once results found, display them
        text.text = f'Classifier returned: {results[0]}'
        print(f'{text.text}')
        for frame in range(MsToFrames(1000, refresh_rate)):
            text.draw()
            win.flip()
        
        # 1000ms blank screen
        for frame in range(MsToFrames(1000, refresh_rate)):
            win.flip()''' 
            
    
########################## Ollies code #####################################
def MsToFrames(ms, fs):
    dt = 1000 / fs;
    return np.round(ms / dt).astype(int);

def lsl_mrk_outlet(name):
    info = pylsl.stream_info(name, 'Markers', 1, 0, pylsl.cf_string, 'ID0123456789');
    outlet = pylsl.stream_outlet(info, 1, 1)
    print('task.py created outlet.')
    return outlet
    
def lsl_inlet(name):
    # Resolve all marker streams
    inlet = None
    tries = 0
    info = pylsl.resolve_stream('name', name)
    inlet = pylsl.stream_inlet(info[0], recover=False)
    print(f'task.py has received the {info[0].type()} inlet.')
    return inlet

if __name__ == "__main__":
    # Set random seed
    random.seed()
    
    # Initialize LSL marker streams
    mrkstream_out = lsl_mrk_outlet('Task_Markers') # important this is first
    results_in = lsl_inlet('Result_Stream')

    # Create PsychoPy window
    win = psychopy.visual.Window(
        screen = 0,
        size=[win_w, win_h],
        units="pix",
        fullscr=False,
        color=bg_color,
        gammaErrorPolicy = "ignore"
    )
    
    # Wait a second for the streams to settle down
    time.sleep(1)
    
    # Run through paradigm
Paradigm(4)