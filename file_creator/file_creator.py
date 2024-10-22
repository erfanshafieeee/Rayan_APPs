def create_cpp_file():
    # دریافت نام فایل از کاربر
    class_name = input("Enter the class name :")
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
	//virtual bool InternalEvaluateExpression(int FormatId, const unsigned char * b,experssion	* Expression);

	const static u16 Class_ID;

	{class_name.upper()}(void);
	~{class_name.upper()}(void);

	//your method
    //exp : bool Value_Configuration(CommandAdorner* Command);

	

private:
}};

#endif //__{class_name.upper()}_H

'''
    # ایجاد فایل و نوشتن قالب در آن
    try:
        with open(cpp_file, 'w') as file:
            file.write(template_cpp)
        print(f"File '{cpp_file}' created successfully with the template.")
        with open(cs_file, 'w') as file:
            file.write(template_cs)
        print(f"File '{cs_file}' created successfully with the template.")
        with open(h_file, 'w') as file:
            file.write(template_h)
        print(f"File '{h_file}' created successfully with the template.")

    except Exception as e:
        print(f"An error occurred while creating the file: {e}")

# اجرای تابع برای ساخت فایل cpp
create_cpp_file()
