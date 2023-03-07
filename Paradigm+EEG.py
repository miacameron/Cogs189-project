import psychopy.visual
import psychopy.event
import time
import numpy as np 
import pylsl
import random

#Global variables
win = None
mrksream_out = None
results_in = None
fixation = None
bg_color = [0,0,0]
win_w = 800 
win_h = 600
refresh_rate = 165

########################## Task Paradigm #####################################
def Paradigm (num_trials = 1): #constructing what our session will look like 
    terminate = False
    
    #Array filled with problems to present 
    problem_set =  ['( 40 ÷ 4(3+2) )^2','3^(8*4) % 3','Compute the second derivative of f(x) = 10x^2 + 8x^3','Compute the second integral of f(x) = 10x + 3x^2 + 7','Compute the second derivative of f(x) = 3x^4 - 4x^2 + 3x + 2','sqrt(400) * 7 - 11^2','Solve for x, x + 27 = ½ + 15 + 2x','Compute the second integral of f(x) = 4x^3 - 19x + 2x^4']
    random.shuffle(problem_set)
    
    #Instructions for entire task 
    intro_text = psychopy.visual.TextStim(win,
                    'Welcome! You will be presented with a series of tasks directed by instructions on the screen.\n\n When you are asked to relax try to clear your mind of any thoughts. When you are asked to solve a problem do so mentally without verbalization. Also try to stay as still as possible throughout the whole session. \n\n Press space when you are ready to begin!', 
                    font='Open Sans', units='pix', 
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
                    'Relax and close your eyes until the experimenter tells you to open your eyes', font='Open Sans', units='pix', 
                    pos=(0,0), alignText='center',
                    height=36, color=[1, 1, 1]
                    )
    
    #Instruct to solve problem
    thinking_text = psychopy.visual.TextStim(win,
                    'Solve the following problem...', font='Open Sans', units='pix', 
                    pos=(0,0), alignText='center',
                    height=36, color=[1, 1, 1]
                    )
                    
    #Conclude Experiment
    end_text = psychopy.visual.TextStim(win,
                    'You are done! Press any key to exit', font='Open Sans', units='pix', 
                    pos=(0,0), alignText='center',
                    height=36, color=[1, 1, 1]
                    )
                    
    for i in range(num_trials):
        #turn trial number into string
        trial = str(i)
        
        #Problem to solve
        problem_text = psychopy.visual.TextStim(win,
                    problem_set[i], font='Open Sans', units='pix', 
                    pos=(0,0), alignText='center',
                    height=36, color=[1, 1, 1]
                    )
    
        if i == 0: # 2000 ms overall instructions at the first trial
            while not psychopy.event.getKeys():
            #for frame in range(MsToFrames(2000, refresh_rate)):
                intro_text.draw()
                win.flip()
            
        # 10000ms prompt to start relaxing
        for frame in range(MsToFrames(10000, refresh_rate)):
            relax_text1.draw()
            win.flip()
            
        # 60000ms blank screen (send LSL marker here)
        for frame in range(MsToFrames(60000, refresh_rate)):
            # Send LSL marker on first frame
            if frame == 0:
                mrkstream_out.push_sample(pylsl.vectorstr([trial]))
            win.flip()
            
        # 10000ms prompt to start problem solving task
        for frame in range(MsToFrames(10000, refresh_rate)):
            thinking_text.draw()
            win.flip()
        
        # 60000ms solve problem screen (send LSL marker here)
        for frame in range(MsToFrames(60000, refresh_rate)):
            # Send LSL marker on first frame
            if frame == 0:
                mrkstream_out.push_sample(pylsl.vectorstr([trial]))
            problem_text.draw()
            win.flip()
            
        # 10000ms prompt to start relaxing again with eyes closed
        for frame in range(MsToFrames(10000, refresh_rate)):
            relax_text2.draw()
            win.flip()
            
        if i == (num_trials-1): # conclude experiment
            while not psychopy.event.getKeys():
            #for frame in range(100):#(MsToFrames(2000, refresh_rate)):
                end_text.draw()
                win.flip()
        #######################End of Paradigm? #############################  
        # Flip screen and send blank
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
        #text.text = f'Classifier returned: {results[0]}'
        #print(f'{text.text}')
        #for frame in range(MsToFrames(1000, refresh_rate)):
            #text.draw()
           # win.flip()
        
        # 1000ms blank screen
        for frame in range(MsToFrames(1000, refresh_rate)):
            win.flip()
            
    
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
    results_in = lsl_inlet('relax_smeb')

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
