

// if (typeof window === 'undefined') {
// console.log('Node.js environment detected.');
// } else {
// console.log('Browser environment detected.');
// }

// // const {
// //         PythonShell: {
// //             run: PythonShell_get_family,
// //             run: PythonShell_get_xlsx,
// //             run: PythonShell_get_input_sale_channel,
// //             run: PythonShell_get_input_production_type,
// //             run: PythonShell_get_stock_source
// //         }
// //     } = require('../../node_modules/python-shell');

// // import PythonShell_get_family from '../../node_modules/python-shell';
// // import PythonShell_get_xlsx from '../../node_modules/python-shell';
// // import PythonShell_get_input_sale_channel from '../../node_modules/python-shell';
// // import PythonShell_get_input_production_type from '../../node_modules/python-shell';
// // import PythonShell_get_stock_source from '../../node_modules/python-shell';

// // import { PythonShell } from '../../node_modules/python-shell';

// // const { PythonShell } = require('python-shell');

// // Run the Python script with the function and arguments
// PythonShell.run('python.py', {args: ['get_family']}, (err, [data]) => {
//     if (err) throw err;
//     document.getElementById("template_options").innerHTML = data;
// });

// PythonShell.run('python.py', {args: ['get_xlsx']}, (err, [data]) => {
//     if (err) throw err;
//     document.getElementById("exist_linesheet").innerHTML = data;
// });

// PythonShell.run('python.py', {args: ['get_input',JSON.stringify('sale_channel','multiple')]}, (err, [data]) => {
//     if (err) throw err;
//     document.getElementById("sale_channel_options").innerHTML = data;
// });

// PythonShell.run('python.py', {args: ['get_input',JSON.stringify('production_type','single')]}, (err, [data]) => {
//     if (err) throw err;
//     document.getElementById("production_type_options").innerHTML = data;
// });



// PythonShell.run('python.py', {args: ['get_input',JSON.stringify('stock_source','multiple')]}, (err, [data]) => {
//     if (err) throw err;
//     document.getElementById("stock_source_options").innerHTML = data;
//     new SlimSelect({
//         select: '#stock_source_show',
//         settings: {
//             closeOnSelect: false,
//             allowDeselectOption: true,
//         },
//         events: {
//             afterChange: (newVal) => {
//                 var input_update ="";
//                 for (let i = 0; i < newVal.length; i++) {
//                     if(input_update==""){
//                         input_update = newVal[i].value;
//                     }else{
//                         input_update = input_update +','+newVal[i].value;
//                     }
//                 }
//                 document.getElementById("stock_source").value = input_update;
//             }
//         }
//     })
//     new SlimSelect({
//         select: '#template_show',
//         settings: {
//             closeOnSelect: false,
//             allowDeselectOption: true,
//         },
//         events: {
//             afterChange: (newVal) => {
//                 var input_update ="";
//                 for (let i = 0; i < newVal.length; i++) {
//                     if(input_update==""){
//                         input_update = newVal[i].value;
//                     }else{
//                         input_update = input_update +','+newVal[i].value;
//                     }
//                 }
//                 document.getElementById("template").value = input_update;
//             }
//         }
//     })
//     new SlimSelect({
//         select: '#sale_channel_show',
//         settings: {
//             closeOnSelect: false,
//             allowDeselectOption: true,
//         },
//         events: {
//             afterChange: (newVal) => {
//                 var input_update ="";
//                 for (let i = 0; i < newVal.length; i++) {
//                     if(input_update==""){
//                         input_update = newVal[i].value;
//                     }else{
//                         input_update = input_update +','+newVal[i].value;
//                     }
//                 }
//                 document.getElementById("sale_channel").value = input_update;
//             }
//         }
//     })
//     new SlimSelect({
//         select: '#production_type_show',
//         settings: {
//             closeOnSelect: false,
//             allowDeselectOption: true,
//         },
//         events: {
//             afterChange: (newVal) => {
//                 var input_update ="";
//                 for (let i = 0; i < newVal.length; i++) {
//                     if(input_update==""){
//                         input_update = newVal[i].value;
//                     }else{
//                         input_update = input_update +','+newVal[i].value;
//                     }
//                 }
//                 document.getElementById("production_type").value = input_update;
//             }
//         }
//     })

// });

