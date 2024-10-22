import tkinter as tk
from tkinter import messagebox
import os
import jdatetime

def create_cpp_file():
    class_name = entry_class_name.get().strip()
    author_name = entry_author_name.get().strip().title()

    if not class_name or not author_name:
        messagebox.showerror("Error", "Class name and author name cannot be empty!")
        return

    # Get the current Shamsi date
    current_date = jdatetime.date.today().strftime("%d/%m/%Y")

    # Create a folder to save the files
    folder_name = class_name.upper()
    os.makedirs(folder_name, exist_ok=True)

    cpp_file = os.path.join(folder_name, class_name.upper() + ".cpp")
    cs_file = os.path.join(folder_name, class_name.upper() + ".cs")
    h_file = os.path.join(folder_name, class_name.upper() + ".h")

    # Template for the cpp file with added name and date
    template_cpp = f'''#include "OtherHeader\\{class_name.upper()}_OH.h"
#include "{class_name.upper()}.h"
#include "MSG_{class_name.upper()}.h"
#include "GeneralSecurity.h"
// #include "AdvancedSelectionForm.h"
// #include "Encoding.h"
// {author_name}-{current_date}

{class_name.upper()}::{class_name.upper()}(void)
{{
}}
//=========================================================================================================================================================================================//
{class_name.upper()}::~{class_name.upper()}(void)
{{
}}
//=========================================================================================================================================================================================//
bool {class_name.upper()}::(yourmetodname)(CommandAdorner *Command)
{{
//your code
}}
'''

    # Template for the cs file
    template_cs = f'''using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using USILogicLayer.Protocol;
using Extensions.ByteArrayExtensions;
using DataAccessLayer;
using System.Threading;
using System.IO;
using Extensions.Loggers;
using USILogicLayer.Algorithms.Algorithm_Forms;
using System.Diagnostics;
using USILogicLayer.Algorithms;

namespace USILogicLayer.Algorithms
{{
    public class {class_name.upper()} : Algorithm
    {{
        public {class_name.upper()}(RayanDataModelDataSet.ECURow ECU, LogicManager logicManager) : base(ECU, logicManager)
        {{
        //your msgs
        }}
    }}
}}
'''

    # Template for the h file
    template_h = f'''#ifndef __{class_name.upper()}_H
#define __{class_name.upper()}_H

#include "rayanmessage.h"
#include "Algorithm.h"

class {class_name.upper()} : public BaseAlgorithm//,VariableAdorner
{{

public:

    virtual bool InternalSwitchCase(CommandAdorner* Command);
    //virtual bool InternalEvaluateExpression(int FormatId, const unsigned char * b,experssion    * Expression);

    const static u16 Class_ID;

    {class_name.upper()}(void);
    ~{class_name.upper()}(void);

    //your method
    //exp : bool Value_Configuration(CommandAdorner* Command);

    

private:
}};

#endif //__{class_name.upper()}_H
'''

    try:
        with open(cpp_file, 'w') as file:
            file.write(template_cpp)
        with open(cs_file, 'w') as file:
            file.write(template_cs)
        with open(h_file, 'w') as file:
            file.write(template_h)
        messagebox.showinfo("Success", f"Files '{cpp_file}', '{cs_file}', and '{h_file}' created successfully in folder '{folder_name}'.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while creating the files: {e}")

# Execute the function when the Enter key is pressed
def on_enter(event):
    create_cpp_file()

# Create the main window
root = tk.Tk()
root.title("C++ and C# Template Generator")
root.geometry("400x300")
root.configure(bg="#0C2D48")  # Carbon blue background

# Add label and entry for class name input
label_class_name = tk.Label(root, text="Enter the class name:", bg="#0C2D48", fg="white")
label_class_name.pack(pady=5)

entry_class_name = tk.Entry(root, width=30)
entry_class_name.pack(pady=5)

# Add label and entry for author name input
label_author_name = tk.Label(root, text="Enter the author name:", bg="#0C2D48", fg="white")
label_author_name.pack(pady=5)

entry_author_name = tk.Entry(root, width=30)
entry_author_name.pack(pady=5)

# Add button to generate files
btn_generate = tk.Button(root, text="Generate Files", command=create_cpp_file, bg="#2E8B57", fg="white")  # Green button
btn_generate.pack(pady=20)

# Bind the Enter key to trigger file generation
root.bind('<Return>', on_enter)

# Run the application
root.mainloop()
