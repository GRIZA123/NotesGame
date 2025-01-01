NOTE_SORT = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")

def set_list_pos(height, notes):
    list_of_pos = [] 
    notes_list = notes.split(" ") 

    for note in notes_list:
        base_note = ''.join([char for char in note if not char.isdigit()])
        if base_note in NOTE_SORT:
            note_index = NOTE_SORT.index(base_note)
            y_pos = (note_index + 1) * (height // 13)

            if list_of_pos:
                last_x = list_of_pos[-1][1][0]
                list_of_pos.append([[last_x, list_of_pos[-1][1][1]], [last_x + 100, y_pos]])
            else:
                list_of_pos.append([[0, 800], [100, y_pos]])
        else:
            print(f"Warning: Note '{note}' is not valid and will be ignored.")

    return list_of_pos

def get_note_height(height, note):
    base_note = ''.join([char for char in note if not char.isdigit()])
    if base_note in NOTE_SORT:
        note_index = NOTE_SORT.index(base_note)
        y_pos = (note_index + 1) * (height // 13)
        return y_pos
    else:
        print(f"Warning: Note '{note}' is not valid.")
        return None

