import tkinter as tk
from tkinter import messagebox

def create_cpp_file():
    class_name = entry_class_name.get().strip()
    if not class_name:
        messagebox.showerror("Error", "Class name cannot be empty!")
        return

    cpp_file = class_name.upper() + ".cpp"
    cs_file = class_name.upper() + ".cs"
    h_file = class_name.upper() + ".h"

    template_cpp = f'''#include "OtherHeader\\{class_name.upper()}_OH.h"
#include "{class_name.upper()}.h"
#include "MSG_{class_name.upper()}.h"
#include "GeneralSecurity.h"
// #include "AdvancedSelectionForm.h"
// #include "Encoding.h"
// Shafiee-06/1403

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
        messagebox.showinfo("Success", f"Files '{cpp_file}', '{cs_file}', and '{h_file}' created successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while creating the files: {e}")

# ایجاد پنجره اصلی
root = tk.Tk()
root.title("C++ and C# Template Generator")
root.geometry("400x200")

# افزودن برچسب و ورودی برای دریافت نام کلاس
label_class_name = tk.Label(root, text="Enter the class name:")
label_class_name.pack(pady=10)

entry_class_name = tk.Entry(root, width=30)
entry_class_name.pack(pady=5)

# افزودن دکمه برای ایجاد فایل‌ها
btn_generate = tk.Button(root, text="Generate Files", command=create_cpp_file, bg="blue", fg="white")
btn_generate.pack(pady=20)

# اجرای برنامه
root.mainloop()
