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
        Set rngDV = Cells.SpecialCells(xlCellTypeAllValidation)
        On Error GoTo exitHandler
        If rngDV Is Nothing Then GoTo exitHandler
        If Intersect(Target, rngDV) Is Nothing Then
           'do nothing
        Else
            If Target.Validation.Type = 3 Then 'Is list validation
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