import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

text = input("Enter the text: ")
pattern = input("Enter the pattern: ")

states = [ ]
match_positions=[]

def record_state(phase, i=None, j=None, lps=None, action=""):
    states.append({
        "phase": phase,
        "i": i,
        "j": j,
        "lps": lps.copy() if lps is not None else None,
        "action": action
    })

def compute_lps(pattern):

    m=len(pattern)
    lps = [0]*m
    length =0
    i = 1

    record_state("lps", i=i, j=length, lps=lps, action="Start building LPS: lps[0]=0")
    while i<m:
        if pattern[i]==pattern[length]:
            length+=1
            lps[i]=length
            record_state("lps", i=i, j=length, lps=lps,
            action=f"Match: pattern[{i}] == pattern[{length-1}], set lps[{i}] = {length}")
            i+=1
        else:
            if length!=0:
                record_state("lps", i=i, j=length, lps=lps,
                action=f"Mismatch: pattern[{i}] != pattern[{length}], jump length to lps[{length-1}]")
                length=lps[length-1]
            else:
                lps[i]=0
                record_state("lps", i=i, j=length, lps=lps,
                action=f"Mismatch with length 0: set lps[{i}] = 0")
                i += 1
    record_state("lps", i=m, j=None, lps=lps, action="Completed LPS array")
    return lps


def kmp_search(text, pattern, lps):

    n = len(text)
    m = len(pattern)
    i=0
    j=0

    record_state("matching", i=i, j=j, lps=lps, action="Start matching phase")
    while i<n:
        if pattern[j]==text[i]:
            record_state("matching", i=i, j=j, lps=lps,
            action=f"Match: text[{i}] == pattern[{j}]")
            i+=1
            j+=1
        else:
            record_state("matching", i=i, j=j, lps=lps,
            action=f"Mismatch: text[{i}] != pattern[{j}]")
            if j!=0:
                j=lps[j-1]
                record_state("matching", i=i, j=j, lps=lps,
                action=f"Jump pattern index to lps[{j}]")
            else:
                i+=1
                record_state("matching", i=i, j=j, lps=lps,
                action=f"No prefix match: move text index to {i}")
        if j==m:
            record_state("matching", i=i, j=j, lps=lps,
            action=f"Found full match ending at text index {i-1}")
            match_positions.append(i - m)
            j=lps[j-1]
            record_state("matching", i=i, j=j, lps=lps,
            action="Restart pattern matching after a full match")

lps=compute_lps(pattern)
kmp_search(text, pattern, lps)

fig, ax = plt.subplots(figsize=(12, 6))
x_start=0.1
dx=0.06
max_possible=x_start+(len(text)+len(pattern)+2)*dx
ax.set_xlim(0,max_possible)
ax.set_ylim(0,1)
plt.axis('off')

text_y = 0.75
pattern_y=0.55
box_height=0.08
box_width=dx

def draw_boxed_letter(ax, letter, center_x, center_y, box_width, box_height,
 font_size=16, color='black', fill_color='none'):
    lower_left = (center_x - box_width/2, center_y - box_height/2)
    rect=Rectangle(lower_left, box_width, box_height,
    edgecolor='black', facecolor=fill_color, lw=1)
    ax.add_patch(rect)
    ax.text(center_x, center_y, letter,
    fontsize=font_size, ha='center', va='center', color=color)

def update(frame):
    ax.clear()
    ax.set_xlim(0, max_possible)
    ax.set_ylim(0, 1)
    plt.axis('off')
    
    state = states[frame]
    phase = state["phase"]
    action=state["action"]

    ax.text(0.5, 0.97, f"Step {frame+1}/{len(states)}: {action}",
    ha='center', va='center', fontsize=12, transform=ax.transAxes)

    if state["lps"] is not None:
        lps_str = "LPS: " + " ".join(str(x) for x in state["lps"])
        ax.text(0.5, 0.93, lps_str, ha='center',
        va='center', fontsize=12, transform=ax.transAxes)

    for idx,char in enumerate(text):
        fill = 'green' if (phase=="matching" and state["i"] is not None and idx==state["i"]) else 'none'
        center_x = x_start + idx * dx
        draw_boxed_letter(ax, char, center_x, text_y, box_width, box_height, fill_color=fill)

    if phase=="lps":
        for idx, char in enumerate(pattern):
            fill = 'red' if (state["i"] is not None and idx == state["i"]) else 'none'
            center_x = x_start + idx * dx
            draw_boxed_letter(ax, char, center_x, pattern_y, box_width, box_height, fill_color=fill)

        if state["i"] is not None and state["j"] is not None:
            xi = x_start + state["i"] * dx
            xj = x_start + state["j"] * dx
            yi = pattern_y + box_height / 2
            yj = pattern_y + box_height / 2
            style="Simple,tail_width=0.5,head_width=6,head_length=8"
            arrow = FancyArrowPatch((xj, yj), (xi, yi),
            connectionstyle="arc3,rad=0.7", arrowstyle=style,
            color="blue", lw=2)
            ax.add_patch(arrow)

    elif phase=="matching":
        pattern_offset = state["i"] - state["j"]
        for idx, char in enumerate(pattern):
            fill = 'orange' if (state["j"] is not None and idx==state["j"]) else 'none'
            center_x = x_start + (pattern_offset + idx) * dx
            draw_boxed_letter(ax, char, center_x, pattern_y, box_width, box_height, fill_color=fill)

        if state["i"] is not None and state["j"] is not None:
            xi = x_start + state["i"] * dx
            xj = x_start + (pattern_offset + state["j"]) * dx
            ax.annotate('', xy=(xj, pattern_y + box_height/2),
            xytext=(xi, text_y - box_height/2),
            arrowprops=dict(arrowstyle="->", color="blue", lw=2))

    if frame == len(states)-1:
        final_text = f"Final: Pattern found at indices {match_positions}"
        ax.text(0.5, 0.1, final_text, ha='center', va='center',
        fontsize=14, transform=ax.transAxes, color='purple')

frame_index = [0]

def manual_update(event):
    if frame_index[0] < len(states):
        update(frame_index[0])
        frame_index[0]+=1
        fig.canvas.draw_idle()
    else:
        print("End of animation.")

plt.ion( )
fig.canvas.mpl_connect('key_press_event', manual_update)
update( 0 )
fig.canvas.draw_idle()
plt.show( block=True )
