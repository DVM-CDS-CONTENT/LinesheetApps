Private Sub Worksheet_Change(ByVal Target As Range)
    Dim wb As Workbook
    Dim ws_linesheet As Worksheet
        Set wb = ActiveWorkbook
        Set ws_linesheet = ActiveWorkbook.Worksheets("IM_FORM")
        Dim Oldvalue As String
        Dim Newvalue As String
        Dim arr_sh() As Boolean
        Dim strArray() As String
        Dim multi_att_se() As String
        Dim select_att As String
        Dim category_label As Integer
        Dim category_label_loop As Integer
        Dim category_label_loop_down As Integer
        Dim logic_first As Integer
        Dim department_column As Integer
        Dim pr_department_column As Integer
Exitsub:
        Application.EnableEvents = True
    '----------end multi select storestock
    '------------old function
        ' Developed by Contextures Inc.
    ' www.contextures.com
        Dim rngDV As Range
        Dim oldVal As String
        Dim newVal As String
        Dim bu As String
        Dim i As Integer
        Dim lUsed  As Integer
        If Target.Count > 1 Then GoTo exitHandler
        On Error Resume Next
        Set rngDV = Cells.SpecialCells(xlCellTypeAllValidation) ' Include C6 in the validation range
        On Error GoTo exitHandler
        If rngDV Is Nothing Then GoTo exitHandler
        If Intersect(Target, rngDV) Is Nothing And Target.Address <> "$C$6" Then
           'do nothing
        Else
           Application.EnableEvents = False
            If Target.Address = "$C$6" Then
                ' Code for multi-select in C6
                ' You can customize this part based on your requirements
                ' For example, you can use a MsgBox to prompt the user for multiple values

                newVal = Target.value
                'Debug.Print "newVal " & newVal
                Application.Undo
                oldVal = Cells(6, 3).value
                Target.value = newVal
                Target.Locked = True
                Debug.Print "oldVal " & oldVal
               If oldVal = "" Then
                    'do nothing
                  Else
                      If newVal = "" Then
                      'do nothing
                      Else
                          lUsed = InStr(1, oldVal, newVal)
                          If lUsed > 0 Then
                              If Right(oldVal, Len(newVal)) = newVal Then
                                  Target.value = Left(oldVal, Len(oldVal) - Len(newVal) - 2)
                              Else
                                  Target.value = Replace(oldVal, newVal & ", ", "")
                              End If
                          Else
                              Target.value = oldVal _
                                  & ", " & newVal
                              '      NOTE: you can use a line break,
                              '      instead of a comma
                              '      Target.Value = oldVal _
                              '        & Chr(10) & newVal
                          End If
                      End If
                  End If

            ElseIf Target.Validation.Type = 3 Then 'Is list validation
              Application.EnableEvents = False
              newVal = Target.value
              Application.Undo
              oldVal = Target.value
              Target.value = newVal
              Target.Locked = True
              Dim chkCol As Boolean
              For i = 1 To 100
                  If InStr(1, Target.EntireColumn.Cells(i), "Multiple Select") > 0 Then
                      chkCol = True
                      Exit For
                  Else
                      chkCol = False
                  End If
              Next
              If chkCol = True Then
                  If oldVal = "" Then
                    'do nothing
                  Else
                      If newVal = "" Then
                      'do nothing
                      Else
                          lUsed = InStr(1, oldVal, newVal)
                          If lUsed > 0 Then
                              If Right(oldVal, Len(newVal)) = newVal Then
                                  Target.value = Left(oldVal, Len(oldVal) - Len(newVal) - 2)
                              Else
                                  Target.value = Replace(oldVal, newVal & ", ", "")
                              End If
                          Else
                              Target.value = oldVal _
                                  & ", " & newVal
                              '      NOTE: you can use a line break,
                              '      instead of a comma
                              '      Target.Value = oldVal _
                              '        & Chr(10) & newVal
                          End If
                      End If
                  End If
              End If
            End If
        End If
exitHandler:
      Application.EnableEvents = True
    '-----------------end old function
  Dim familyTemplateSheet As Worksheet
    Dim imFormSheet As Worksheet
    Dim imFormCategoriesRange As Range
    Dim imFormRange As Range
    Dim categoryColIndex As Long
    Dim categoryCell As Range
    Dim attributeRange As Range
    Dim category As String
    Dim attributesInFamily As String
    Dim attributesInIM As String
    Dim mismatch As Boolean
    Dim lastColumn As Long

    On Error Resume Next
    Set familyTemplateSheet = ThisWorkbook.Sheets("FAMILY_TEMPLATE")
    Set imFormSheet = ThisWorkbook.Sheets("IM_FORM")
    On Error GoTo 0

    If familyTemplateSheet Is Nothing Or imFormSheet Is Nothing Then Exit Sub ' Exit if sheets don't exist

    ' Find the column index of the "online_categories" header
    On Error Resume Next
    categoryColIndex = Application.WorksheetFunction.Match("online_categories", imFormSheet.Rows(1), 0)
    categoryColIndexSet = Application.WorksheetFunction.Match("categories", familyTemplateSheet.Rows(1), 0)
    On Error GoTo 0

    If categoryColIndex = 0 Then
        'Debug.Print "Column 'online_categories' not found in IM_FORM sheet."
        'Call HighlightEmptyCellUnderRequire
        'Exit Sub ' Exit if "online_categories" header not found
    Else

    Debug.Print "Column 'online_categories' found at index: " & categoryColIndex
    Dim selectedRow As Long
    selectedRow = ActiveCell.Row

    Set imFormCategoriesRange = imFormSheet.Range(imFormSheet.Cells(selectedRow, categoryColIndex), imFormSheet.Cells(selectedRow, categoryColIndex))
    Set familyCategoriesRange = familyTemplateSheet.Range(familyTemplateSheet.Cells(2, categoryColIndexSet), familyTemplateSheet.Cells(familyTemplateSheet.Cells(familyTemplateSheet.Rows.Count, categoryColIndexSet).End(xlUp).Row, categoryColIndexSet))
    Set imFormRange = imFormSheet.Range("A2", imFormSheet.Cells(imFormSheet.Cells(imFormSheet.Rows.Count, imFormSheet.Columns.Count).End(xlUp).Row, imFormSheet.Columns.Count))



    Application.EnableEvents = False ' Prevent triggering events while making changes

    For Each categoryCell In imFormCategoriesRange.Cells
        category = categoryCell.value

        attributesInFamily = ""
        attributesInIM = ""
        mismatch = False
        If category <> "" Then

            ' Debug.Print "Processing category: " & category

            ' Find the attributes associated with the category in FAMILY_TEMPLATE
            Dim attributeColumnIndex As Long
            attributeColumnIndex = 0
            For i = 1 To familyTemplateSheet.Cells(1, familyTemplateSheet.Columns.Count).End(xlToLeft).Column

                If familyTemplateSheet.Cells(1, i).value = "categories" Then
                    attributeColumnIndex = i
                    Exit For
                End If
            Next i
            'Debug.Print "attributeColumnIndex: " & attributeColumnIndex

            ' Find the attributes associated with the category in FAMILY_TEMPLATE
            Dim categoryRow As Range
            Set categoryRow = familyCategoriesRange.Find(category, LookIn:=xlValues, LookAt:=xlWhole)

            For j = 2 To 5
                If categoryRow Is Nothing Then
                   'Debug.Print "skip: " & category
                Else
                    If attributeColumnIndex > 0 Then
                        attributesInFamily = familyTemplateSheet.Cells(familyCategoriesRange.Find(category).Row, j).value
                    End If

                    'Debug.Print "attributesInFamily: " & attributesInFamily

                    ' Highlight cells in the current row based on attributesInFamily
                    If attributesInFamily <> "" Then
                        Dim attributesArray As Variant
                        attributesArray = Split(attributesInFamily, ",")

                        For Each att In attributesArray
                            Dim attributeColumn As Range
                            On Error Resume Next
                            Set attributeColumn = imFormRange.Rows(1).Find(att, LookIn:=xlValues, LookAt:=xlWhole)
                            On Error GoTo 0

                            If Not attributeColumn Is Nothing Then
                                If j = 3 Then
                                    If imFormSheet.Cells(categoryCell.Row, attributeColumn.Column) = "" Then
                                        imFormSheet.Cells(categoryCell.Row, attributeColumn.Column).Interior.Color = RGB(255, 143, 143) ' Highlight in r
                                    Else
                                        imFormSheet.Cells(categoryCell.Row, attributeColumn.Column).Interior.Color = RGB(255, 255, 255) ' Highlight in r
                                    End If
                                ElseIf j = 4 Then
                                    imFormSheet.Cells(categoryCell.Row, attributeColumn.Column).Interior.Color = RGB(255, 255, 255) ' Highlight in 0
                                ElseIf j = 5 Then
                                    imFormSheet.Cells(categoryCell.Row, attributeColumn.Column).Interior.Color = RGB(231, 231, 231) ' Highlight in AO
                                ElseIf j = 6 Then
                                    imFormSheet.Cells(categoryCell.Row, attributeColumn.Column).Interior.Color = RGB(231, 231, 231) ' Highlight in AR
                                ElseIf j = 7 Then
                                    imFormSheet.Cells(categoryCell.Row, attributeColumn.Column).Interior.Color = RGB(231, 231, 231) ' Highlight in AR
                                End If
                            End If
                        Next att
                    End If
                End If
            Next j
        End If
Skiptonextcategories:
    Next categoryCell
 End If

Application.EnableEvents = True ' Re-enable events

    End Sub
    Public Function FindColbo(rng As Range, srchVal As Variant) As Long
        Dim Found As Range
        With rng
            Set Found = .Find(What:=srchVal, _
                                LookIn:=xlValues, _
                                LookAt:=xlWhole, _
                                SearchOrder:=xlByRows, _
                                SearchDirection:=xlNext, _
                                MatchCase:=True)
        End With
        If Not Found Is Nothing Then
            FindColbo = Found.Column
        Else
            FindColbo = 0
        End If
    End Function
    Function IsInArray(stringToBeFound As String, arr As Variant) As Boolean
        IsInArray = Not IsError(Application.Match(stringToBeFound, arr, 0))
    End Function
    Public Function FindRow(rng As Range, srchVal As String) As Long
        Dim Found As Range
        With rng
            Set Found = .Find(What:=srchVal, _
                                LookIn:=xlValues, _
                                LookAt:=xlPart, _
                                SearchOrder:=xlByColumns, _
                                SearchDirection:=xlNext, _
                                MatchCase:=True)
        End With
        If Not Found Is Nothing Then
            FindRow = Found.Row
        Else
            FindRow = 0
        End If
    End Function
    Public Function FindCol(rng As Range, srchVal As String) As Long
        Dim Found As Range
        With rng
            Set Found = .Find(What:=srchVal, _
                                LookIn:=xlValues, _
                                LookAt:=xlPart, _
                                SearchOrder:=xlByRows, _
                                SearchDirection:=xlNext, _
                                MatchCase:=True)
        End With
        If Not Found Is Nothing Then
            FindCol = Found.Column
        Else
            FindCol = 0
        End If
    End Function
    Function lookupAtb(lookupSheet As Worksheet, value)
        Dim lookupRange As Range
        Dim valCol As Integer
        Set lookupRange = lookupSheet.Range("color_table")
        valCol = 2
        On Error Resume Next
        lookupAtb = Application.WorksheetFunction.VLookup(value, lookupRange, valCol, False)
        If Err.Number <> 0 Then
            lookupAtb = "N/A"
        End If
    End Function

Sub HighlightEmptyCellUnderRequire()

    Dim ws As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim targetColumn As Long

    ' Set the worksheet
    Set ws = ThisWorkbook.Sheets("IM_FORM") ' Replace "YourSheetName" with the actual name of your sheet

    ' Find the target column (assuming "IBC" is in the first row)
    On Error Resume Next
    IBCcolumn = ws.Rows(1).Find("ibc").Column
    On Error GoTo 0

    ' Check if the target column is found
    If IBCcolumn = 0 Then
        MsgBox "Column 'IBC' not found!", vbExclamation
        Exit Sub
    End If

    ' Find the last row with data in the target column

    lastRow = ws.Cells(ws.Rows.Count, IBCcolumn).End(xlUp).Row
    lastColumn = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column


    ' Loop through each row starting from row 2 (assuming headers are in row 1)
    For i = 2 To lastRow
        For ColCheck = 1 To lastColumn
            ' Check if the value in column A contains "Require" (case-insensitive)
            If InStr(1, UCase(ws.Cells(i, ColCheck).value), "Require", vbTextCompare) > 0 Then
                ' Check if the cell under the "IBC" column is empty
                For j = i To lastRow
                    If Not IsEmpty(ws.Cells(j + 2, IBCcolumn).value) Then
                        ' Highlight the cell under the "IBC" column in red
                        If IsEmpty(ws.Cells(j + 2, ColCheck).value) Then
                            ws.Cells(j + 2, ColCheck).Interior.Color = RGB(255, 143, 143)
                        Else
                            ws.Cells(j + 2, ColCheck).Interior.Color = xlNone
                        End If
                    End If
                Next j
            End If
        Next ColCheck
    Next i
End Sub
Sub HighlightedCellsInfo()
    Dim ws As Worksheet
    Dim InlinkDataSheet As Worksheet
    Dim rng As Range
    Dim cell As Range
    Dim lastRow As Long
    Dim IDSlastRow As Long
    Dim currentRow As Long
    Dim highlightedCells As String

    ' Set the worksheet and range to be checked
    Set ws = ThisWorkbook.Sheets("IM_FORM") ' Change "Sheet1" to your actual sheet name

    Set rng = ws.UsedRange ' You can modify the range as needed

    ' Initialize variables
    lastRow = rng.Rows.Count
    currentRow = 0
    highlightedCells = ""

    ' Loop through each cell in the specified range
    For Each cell In rng
        ' Check if the cell's interior color is RGB(255, 143, 143)
        If cell.Interior.Color = RGB(255, 143, 143) Then
            ' Check if the cell is in the same row as the previous one
            If cell.Row <> currentRow Then
                ' If not the first row, add a new line
                If currentRow <> 0 Then
                    highlightedCells = highlightedCells & vbCrLf
                End If
                ' Record the row and column information
                highlightedCells = highlightedCells & "Error : Row: " & cell.Row & ", Columns: " & ColumnToLetter(cell.Column) & " is missing require value" & vbCrLf
            Else
                ' If the cell is in the same row, append the column information
                highlightedCells = highlightedCells & "Error :  Row: " & cell.Row & ", Columns: " & ColumnToLetter(cell.Column) & " is missing require value" & vbCrLf
            End If

            ' Update the current row
            currentRow = cell.Row
        End If
    Next cell

    ' Display the recorded information in a message box
    If highlightedCells <> "" Then
      ' Set the worksheet
        Set InlinkDataSheet = ThisWorkbook.Sheets("IN_LINK_DATA")
        IDSlastRow = InlinkDataSheet.Cells(InlinkDataSheet.Rows.Count, 1).End(xlUp).Row

        For i = 1 To IDSlastRow
            If InlinkDataSheet.Cells(i, 1).value = "msg_validate_mandatory_checking" Then
                InlinkDataSheet.Cells(i, 2).value = highlightedCells
            End If
        Next i

        MsgBox highlightedCells
    Else
        Set InlinkDataSheet = ThisWorkbook.Sheets("IN_LINK_DATA")
        For i = 1 To IDSlastRow
            If InlinkDataSheet.Cells(i, 1).value = "msg_validate_mandatory_checking" Then
                InlinkDataSheet.Cells(i, 2).value = "Passed : No cells with the require is missing."
            End If
        Next i

        MsgBox "Passed : No cells with the require is missing."
    End If
End Sub




Private Sub Workbook_SheetFollowHyperlink(ByVal Sh As Object, ByVal Target As Hyperlink)
    If Target.Range.Address = "$F$4" Then
        Call HighlightEmptyCellUnderRequire
        Call HighlightedCellsInfo
    End If
End Sub

Sub HighlightWrongTypeValue()

    Dim ws As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim targetColumn As Long
    Dim status As Integer


    Warning_Message = ""

    ' Set the worksheet
    Set ws = ThisWorkbook.Sheets("IM_FORM") ' Replace "YourSheetName" with the actual name of your sheet

    ' Find the target column (assuming "IBC" is in the first row)
    On Error Resume Next
    IBCcolumn = ws.Rows(1).Find("ibc").Column
    On Error GoTo 0

    ' Check if the target column is found
    If IBCcolumn = 0 Then
        MsgBox "Column 'IBC' not found!", vbExclamation
        Exit Sub
    End If

    ' Find the last row with data in the target column
    lastRow = ws.Cells(ws.Rows.Count, IBCcolumn).End(xlUp).Row
    lastColumn = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column


    ' Loop through each row starting from row 2 (assuming headers are in row 1)
    For i = 2 To lastRow
        For ColCheck = 1 To lastColumn
            ' Check if the value in column A contains "Require" (case-insensitive)
            If InStr(1, UCase(ws.Cells(i, ColCheck).value), "Formula", vbTextCompare) > 0 Or _
            InStr(1, UCase(ws.Cells(i, ColCheck).Formula), "Number only", vbTextCompare) > 0 Or _
            InStr(1, UCase(ws.Cells(i, ColCheck).Formula), "Simple Select", vbTextCompare) > 0 Or _
            InStr(1, UCase(ws.Cells(i, ColCheck).Formula), "Multiple Select", vbTextCompare) > 0 Or _
            InStr(1, UCase(ws.Cells(i, ColCheck).Formula), "link", vbTextCompare) > 0 _
            Then
                ' Check if the cell under the "IBC" column is empty
                For j = i To lastRow
                     If Not IsEmpty(ws.Cells(j + 6, IBCcolumn).value) Then
                      'check type

                          If Not ws.Cells(j + 6, ColCheck).value = "" Then
                            If ws.Cells(i, ColCheck).value = "Formula" Then
                                If Not ws.Cells(j + 6, ColCheck).HasFormula Then
                                    Warning_Message = Warning_Message & "Value at row  " & j + 6 & " Column " & ColumnToLetter(CInt(ColCheck)) & " " & ws.Cells(1, ColCheck).value & " not a " & ws.Cells(i, ColCheck).value & " type" & vbCrLf
                                End If
                            ElseIf ws.Cells(i, ColCheck).value = "Number only" Then
                                If Not IsNumeric(ws.Cells(j + 6, ColCheck).value) Then
                                    Warning_Message = Warning_Message & "Value at row  " & j + 6 & " Column " & ColumnToLetter(CInt(ColCheck)) & " " & ws.Cells(1, ColCheck).value & " not a " & ws.Cells(i, ColCheck).value & " type" & vbCrLf
                                End If

                            ElseIf ws.Cells(i, ColCheck).value = "link" Then

                                If ws.Cells(j + 6, ColCheck).Hyperlinks.Count > 0 Then
                                    If CheckHyperlinkStatus(ws.Cells(j + 6, ColCheck).value) <> 200 And CheckHyperlinkStatus(ws.Cells(j + 6, ColCheck).Hyperlinks(1).Address) <> 200 Then
                                        Warning_Message = Warning_Message & "The link at row " & j + 6 & " Column " & ColumnToLetter(CInt(ColCheck)) & " " & ws.Cells(1, ColCheck).value & " is invalid" & vbCrLf
                                    End If
                                Else
                                    Warning_Message = Warning_Message & "The link at row " & j + 6 & " Column " & ColumnToLetter(CInt(ColCheck)) & " " & ws.Cells(1, ColCheck).value & " is invalid" & vbCrLf
                                End If

                            ElseIf ws.Cells(i, ColCheck).value = "Simple Select" Then


                                If CheckDropdownList(ws.Cells(j + 6, ColCheck).value, ws.Cells(1, ColCheck).value) = False Then
                                    Warning_Message = Warning_Message & "the value at row " & j + 6 & " Column " & ColumnToLetter(CInt(ColCheck)) & " " & ws.Cells(1, ColCheck).value & " is not indropdown list " & vbCrLf
                                End If
                            End If



                      End If
                      'end check type

                    End If
                Next j
            End If
        Next ColCheck
    Next i
    If Warning_Message <> "" Then

        ' Set the worksheet
        Set InlinkDataSheet = ThisWorkbook.Sheets("IN_LINK_DATA")
        IDSlastRow = ws.Cells(InlinkDataSheet.Rows.Count, 1).End(xlUp).Row

        For i = 1 To lastRow
            If InlinkDataSheet.Cells(i, 1).value = "msg_validate_type_checking" Then
                InlinkDataSheet.Cells(i, 2).value = Warning_Message
            End If
        Next i



        MsgBox "Type Checking: " & vbCrLf & Warning_Message
    Else
        Set InlinkDataSheet = ThisWorkbook.Sheets("IN_LINK_DATA")
        InlinkDataSheet.Cells(i, 2).value = "Passed : All of value follow type of attribtue"
        MsgBox "Passed : All of value follow type of attribtue"
    End If
End Sub
Function GetLinkStatus(link As String) As Integer
    On Error Resume Next
    Dim xmlhttp As Object: Set xmlhttp = CreateObject("MSXML2.ServerXMLHTTP")
    xmlhttp.Open "HEAD", link, False
    xmlhttp.send
    GetLinkStatus = xmlhttp.status
    On Error GoTo 0
End Function

Function CheckHyperlinkStatus(link As String) As Integer
    CheckHyperlinkStatus = GetLinkStatus(link)
End Function
Function CheckDropdownList(value_in_cell As Variant, name_tag As String) As Boolean
    Dim ws As Worksheet
    Dim validationList As Variant
    Dim namedRange As Range
    Dim allowedValues() As Variant
    Dim i As Long

    ' Assuming you have a reference to the worksheet
    ' Replace "IM_FORM" with the actual sheet name
    Set ws = ThisWorkbook.Sheets("ATT_OPTION")

    ' Check if the named range exists
    On Error Resume Next
    Set namedRange = ws.Range(name_tag)


    On Error GoTo 0

    If Not namedRange Is Nothing Then
        ' Get the allowed values from the named range
        validationList = namedRange.value

        ' Convert the validationList to a dynamic array
        'ReDim allowedValues(1 To UBound(validationList))

        If VarType(validationList) = vbString Then
             If value_in_cell = validationList Then
                CheckDropdownList = True
             Else
                CheckDropdownList = False
             End If
        Else
             CheckDropdownList = IsValueInArray(value_in_cell, validationList)
        End If
        ' Check if the value is in the named range




    Else
        ' If the named range doesn't exist, return False
        CheckDropdownList = False
    End If
End Function
Function IsValueInArray(value As Variant, arr As Variant) As Boolean
    Dim i As Long
    For i = 1 To UBound(arr)
        If arr(i, 1) = value Then
            IsValueInArray = True
            GoTo ext
        End If
    Next i

    IsValueInArray = False
ext:

End Function

Function ColumnToLetter(col As Integer) As String
    Dim temp As Integer
    Dim letter As String
    temp = col
    letter = ""
    Do While temp > 0
        letter = Chr(((temp - 1) Mod 26) + 65) & letter
        temp = (temp - 1) \ 26
    Loop
    ColumnToLetter = letter
End Function




Sub StoreStockValidateion()

    Dim wb As Workbook
    Dim ws_linesheet As Worksheet
    Dim i As Integer
    Dim BrandValidation As Boolean
    Dim current_store_this_brand As String
    Dim store_stock As String
    Dim Brandcolumn As Integer
    Dim IBCcolumn As Integer
    Dim dataArray() As String
    Dim uniqueArray() As String
    Dim WarningMessage As String



    Set wb = ActiveWorkbook
    Set ws_linesheet = ActiveWorkbook.Worksheets("IM_FORM")
    Set ws_brand_store_mapping = ActiveWorkbook.Worksheets("BRAND_STORE_MAPPING")

    store_stock = ws_linesheet.Range("C6").value
    If store_stock = "" Then
        MsgBox "Not found store stock selected"
        GoTo missing_store_stock
    End If
    store_stock_array = Split(store_stock, ",")



    For i = LBound(store_stock_array) To UBound(store_stock_array)
        store_stock_array(i) = Trim(store_stock_array(i))
    Next i

    Brandcolumn = ws_linesheet.Rows(1).Find("brand_name").Column
    IBCcolumn = ws_linesheet.Rows(1).Find("ibc").Column

    Dim lastRow As Long
    lastRow_linesheet = ws_linesheet.Cells(ws_linesheet.Rows.Count, IBCcolumn).End(xlUp).Row
    lastRow_mapping = ws_brand_store_mapping.Cells(ws_brand_store_mapping.Rows.Count, 1).End(xlUp).Row
    lastColumn_mapping = ws_brand_store_mapping.Cells(1, ws_brand_store_mapping.Columns.Count).End(xlToLeft).Column

    'find first data row
    For i = 1 To lastRow_linesheet
        If ws_linesheet.Cells(i, 1).value = "No." Then
            StartDataRow = i
              Exit For
        End If
    Next i

    StartDataRow = StartDataRow + 1

    'loop in data then check the stock

    For i = StartDataRow To lastRow_linesheet
        brand_name = ws_linesheet.Cells(i, Brandcolumn).value
        BrandValidation = False

            If brand_name = "" Then
                WarningMessage = WarningMessage & "brand name (" & ColumnToLetter(CInt(Brandcolumn)) & ") at row " & i & " is empty " & vbCrLf
                GoTo missing_brand 'skip this sku
            End If

        'get store avalibale for brand ablove

         For j = 1 To lastRow_mapping
            If UCase(ws_brand_store_mapping.Cells(j, 1).value) = UCase(brand_name) Then
                BrandValidation = True
                For k = 1 To lastColumn_mapping

                    status_store_this_brand = ws_brand_store_mapping.Cells(j, k).value
                    current_store_this_brand = ws_brand_store_mapping.Cells(1, k).value


                    If status_store_this_brand = "Allow" Then
                        If IsInArray(current_store_this_brand, store_stock_array) = False Then
                            WarningMessage = WarningMessage & "Warning : " & current_store_this_brand & " is required for brand " & brand_name & vbCrLf

                        End If
                    Else
                        If IsInArray(current_store_this_brand, store_stock_array) = True Then
                            WarningMessage = WarningMessage & "Warning : " & current_store_this_brand & " is not avalible for brand " & brand_name & vbCrLf

                        End If

                    End If

                Next k
            End If
            If BrandValidation = False And j = lastRow_mapping Then
                WarningMessage = WarningMessage & "Passed : not found brand " & brand_name & " in validation mapping" & vbCrLf
            End If
         Next j

missing_brand:

    Next i

    If Not WarningMessage = "" Then
        dataArray = Split(WarningMessage, vbCrLf)
        uniqueArray = RemoveDuplicatesFromArray(dataArray)
        WarningMessage = Join(uniqueArray, vbCrLf)
    Else
        WarningMessage = "Passed : All of stock in each brand is valid"

    End If

    MsgBox WarningMessage

missing_store_stock:
End Sub

Function RemoveDuplicatesFromArray(inputArray() As String) As String()
    Dim uniqueArray() As String
    Dim dict As Object
    Set dict = CreateObject("Scripting.Dictionary")

    Dim i As Integer
    For i = LBound(inputArray) To UBound(inputArray)
        If Not dict.Exists(inputArray(i)) Then
            dict.Add inputArray(i), Nothing
        End If
    Next i

    ReDim uniqueArray(0 To dict.Count - 1)

    i = 0
    For Each Key In dict.Keys
        uniqueArray(i) = Key
        i = i + 1
    Next Key

    RemoveDuplicatesFromArray = uniqueArray
End Function
Sub RunValidation()
    Call HighlightEmptyCellUnderRequire
    Call HighlightedCellsInfo
    Call HighlightWrongTypeValue
    Call StoreStockValidateion
End Sub























