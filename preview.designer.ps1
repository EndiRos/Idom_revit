$UI_crea_sheet = New-Object -TypeName System.Windows.Forms.Form
[System.Windows.Forms.FlowLayoutPanel]$Vews_list = $null
[System.Windows.Forms.Button]$create_button = $null
[System.Windows.Forms.Button]$Cancel_button = $null
[System.Windows.Forms.Label]$sheet_name = $null
[System.Windows.Forms.FlowLayoutPanel]$S_views = $null
[System.Windows.Forms.Label]$Label1 = $null
[System.Windows.Forms.ComboBox]$S_Collection = $null
[System.Windows.Forms.GroupBox]$GroupBox1 = $null
[System.Windows.Forms.NumericUpDown]$Num_pag = $null
[System.Windows.Forms.CheckBox]$CheckBox1 = $null
[System.Windows.Forms.Label]$Label2 = $null
[System.Windows.Forms.ComboBox]$S_Titlebolock = $null
[System.Windows.Forms.Label]$Label3 = $null
[System.Windows.Forms.Label]$S_Sheet_Title = $null
[System.Windows.Forms.TextBox]$S_sheet_name = $null
[System.Windows.Forms.TextBox]$TextBox1 = $null
function InitializeComponent
{
$Vews_list = (New-Object -TypeName System.Windows.Forms.FlowLayoutPanel)
$create_button = (New-Object -TypeName System.Windows.Forms.Button)
$Cancel_button = (New-Object -TypeName System.Windows.Forms.Button)
$sheet_name = (New-Object -TypeName System.Windows.Forms.Label)
$S_views = (New-Object -TypeName System.Windows.Forms.FlowLayoutPanel)
$Label1 = (New-Object -TypeName System.Windows.Forms.Label)
$S_Collection = (New-Object -TypeName System.Windows.Forms.ComboBox)
$GroupBox1 = (New-Object -TypeName System.Windows.Forms.GroupBox)
$Num_pag = (New-Object -TypeName System.Windows.Forms.NumericUpDown)
$CheckBox1 = (New-Object -TypeName System.Windows.Forms.CheckBox)
$Label2 = (New-Object -TypeName System.Windows.Forms.Label)
$S_Titlebolock = (New-Object -TypeName System.Windows.Forms.ComboBox)
$Label3 = (New-Object -TypeName System.Windows.Forms.Label)
$S_Sheet_Title = (New-Object -TypeName System.Windows.Forms.Label)
$S_sheet_name = (New-Object -TypeName System.Windows.Forms.TextBox)
$TextBox1 = (New-Object -TypeName System.Windows.Forms.TextBox)
$GroupBox1.SuspendLayout()
([System.ComponentModel.ISupportInitialize]$Num_pag).BeginInit()
$UI_crea_sheet.SuspendLayout()
#
#Vews_list
#
$Vews_list.AllowDrop = $true
$Vews_list.Location = (New-Object -TypeName System.Drawing.Point -ArgumentList @([System.Int32]44,[System.Int32]33))
$Vews_list.Name = [System.String]'Vews_list'
$Vews_list.Size = (New-Object -TypeName System.Drawing.Size -ArgumentList @([System.Int32]205,[System.Int32]302))
$Vews_list.TabIndex = [System.Int32]0
#
#create_button
#
$create_button.Location = (New-Object -TypeName System.Drawing.Point -ArgumentList @([System.Int32]166,[System.Int32]564))
$create_button.Name = [System.String]'create_button'
$create_button.Size = (New-Object -TypeName System.Drawing.Size -ArgumentList @([System.Int32]86,[System.Int32]28))
$create_button.TabIndex = [System.Int32]1
$create_button.Text = [System.String]'Ok'
$create_button.UseVisualStyleBackColor = $true
$create_button.add_Click($Button1_Click)
#
#Cancel_button
#
$Cancel_button.Location = (New-Object -TypeName System.Drawing.Point -ArgumentList @([System.Int32]306,[System.Int32]567))
$Cancel_button.Name = [System.String]'Cancel_button'
$Cancel_button.Size = (New-Object -TypeName System.Drawing.Size -ArgumentList @([System.Int32]86,[System.Int32]25))
$Cancel_button.TabIndex = [System.Int32]2
$Cancel_button.Text = [System.String]'Cancel'
$Cancel_button.UseVisualStyleBackColor = $true
#
#sheet_name
#
$sheet_name.Location = (New-Object -TypeName System.Drawing.Point -ArgumentList @([System.Int32]24,[System.Int32]27))
$sheet_name.Name = [System.String]'sheet_name'
$sheet_name.Size = (New-Object -TypeName System.Drawing.Size -ArgumentList @([System.Int32]124,[System.Int32]20))
$sheet_name.TabIndex = [System.Int32]3
$sheet_name.Text = [System.String]'Nombre de la coleccion:'
$sheet_name.TextAlign = [System.Drawing.ContentAlignment]::TopRight
#
#S_views
#
$S_views.Location = (New-Object -TypeName System.Drawing.Point -ArgumentList @([System.Int32]302,[System.Int32]33))
$S_views.Name = [System.String]'S_views'
$S_views.Size = (New-Object -TypeName System.Drawing.Size -ArgumentList @([System.Int32]207,[System.Int32]302))
$S_views.TabIndex = [System.Int32]4
#
#Label1
#
$Label1.Location = (New-Object -TypeName System.Drawing.Point -ArgumentList @([System.Int32]56,[System.Int32]180))
$Label1.Name = [System.String]'Label1'
$Label1.Size = (New-Object -TypeName System.Drawing.Size -ArgumentList @([System.Int32]92,[System.Int32]20))
$Label1.TabIndex = [System.Int32]6
$Label1.Text = [System.String]'Nº de Pagina :'
$Label1.TextAlign = [System.Drawing.ContentAlignment]::TopRight
$Label1.add_Click($Label1_Click)
#
#S_Collection
#
$S_Collection.FormattingEnabled = $true
$S_Collection.Location = (New-Object -TypeName System.Drawing.Point -ArgumentList @([System.Int32]154,[System.Int32]24))
$S_Collection.Name = [System.String]'S_Collection'
$S_Collection.Size = (New-Object -TypeName System.Drawing.Size -ArgumentList @([System.Int32]219,[System.Int32]21))
$S_Collection.TabIndex = [System.Int32]7
#
#GroupBox1
#
$GroupBox1.Controls.Add($Vews_list)
$GroupBox1.Controls.Add($S_views)
$GroupBox1.Location = (New-Object -TypeName System.Drawing.Point -ArgumentList @([System.Int32]12,[System.Int32]215))
$GroupBox1.Name = [System.String]'GroupBox1'
$GroupBox1.Size = (New-Object -TypeName System.Drawing.Size -ArgumentList @([System.Int32]548,[System.Int32]346))
$GroupBox1.TabIndex = [System.Int32]8
$GroupBox1.TabStop = $false
$GroupBox1.Text = [System.String]'Selecciona vistas'
#
#Num_pag
#
$Num_pag.Enabled = $false
$Num_pag.Location = (New-Object -TypeName System.Drawing.Point -ArgumentList @([System.Int32]154,[System.Int32]178))
$Num_pag.Name = [System.String]'Num_pag'
$Num_pag.Size = (New-Object -TypeName System.Drawing.Size -ArgumentList @([System.Int32]43,[System.Int32]21))
$Num_pag.TabIndex = [System.Int32]9
#
#CheckBox1
#
$CheckBox1.Location = (New-Object -TypeName System.Drawing.Point -ArgumentList @([System.Int32]314,[System.Int32]176))
$CheckBox1.Name = [System.String]'CheckBox1'
$CheckBox1.Size = (New-Object -TypeName System.Drawing.Size -ArgumentList @([System.Int32]104,[System.Int32]24))
$CheckBox1.TabIndex = [System.Int32]11
$CheckBox1.Text = [System.String]'Incremental '
$CheckBox1.UseVisualStyleBackColor = $true
#
#Label2
#
$Label2.Location = (New-Object -TypeName System.Drawing.Point -ArgumentList @([System.Int32]48,[System.Int32]146))
$Label2.Name = [System.String]'Label2'
$Label2.Size = (New-Object -TypeName System.Drawing.Size -ArgumentList @([System.Int32]100,[System.Int32]23))
$Label2.TabIndex = [System.Int32]12
$Label2.Text = [System.String]'Formato: '
$Label2.TextAlign = [System.Drawing.ContentAlignment]::TopRight
#
#S_Titlebolock
#
$S_Titlebolock.FormattingEnabled = $true
$S_Titlebolock.Location = (New-Object -TypeName System.Drawing.Point -ArgumentList @([System.Int32]154,[System.Int32]143))
$S_Titlebolock.Name = [System.String]'S_Titlebolock'
$S_Titlebolock.Size = (New-Object -TypeName System.Drawing.Size -ArgumentList @([System.Int32]219,[System.Int32]21))
$S_Titlebolock.TabIndex = [System.Int32]13
#
#Label3
#
$Label3.Location = (New-Object -TypeName System.Drawing.Point -ArgumentList @([System.Int32]48,[System.Int32]66))
$Label3.Name = [System.String]'Label3'
$Label3.Size = (New-Object -TypeName System.Drawing.Size -ArgumentList @([System.Int32]100,[System.Int32]23))
$Label3.TabIndex = [System.Int32]14
$Label3.Text = [System.String]'Nombre de la hoja:  '
$Label3.add_Click($Label3_Click)
#
#S_Sheet_Title
#
$S_Sheet_Title.Location = (New-Object -TypeName System.Drawing.Point -ArgumentList @([System.Int32]48,[System.Int32]108))
$S_Sheet_Title.Name = [System.String]'S_Sheet_Title'
$S_Sheet_Title.Size = (New-Object -TypeName System.Drawing.Size -ArgumentList @([System.Int32]100,[System.Int32]23))
$S_Sheet_Title.TabIndex = [System.Int32]15
$S_Sheet_Title.Text = [System.String]'titulo plano: '
$S_Sheet_Title.TextAlign = [System.Drawing.ContentAlignment]::TopRight
#
#S_sheet_name
#
$S_sheet_name.Location = (New-Object -TypeName System.Drawing.Point -ArgumentList @([System.Int32]154,[System.Int32]63))
$S_sheet_name.Name = [System.String]'S_sheet_name'
$S_sheet_name.Size = (New-Object -TypeName System.Drawing.Size -ArgumentList @([System.Int32]219,[System.Int32]21))
$S_sheet_name.TabIndex = [System.Int32]16
#
#TextBox1
#
$TextBox1.Location = (New-Object -TypeName System.Drawing.Point -ArgumentList @([System.Int32]154,[System.Int32]105))
$TextBox1.Name = [System.String]'TextBox1'
$TextBox1.Size = (New-Object -TypeName System.Drawing.Size -ArgumentList @([System.Int32]219,[System.Int32]21))
$TextBox1.TabIndex = [System.Int32]17
#
#UI_crea_sheet
#
$UI_crea_sheet.ClientSize = (New-Object -TypeName System.Drawing.Size -ArgumentList @([System.Int32]572,[System.Int32]632))
$UI_crea_sheet.Controls.Add($TextBox1)
$UI_crea_sheet.Controls.Add($S_sheet_name)
$UI_crea_sheet.Controls.Add($S_Sheet_Title)
$UI_crea_sheet.Controls.Add($Label3)
$UI_crea_sheet.Controls.Add($S_Titlebolock)
$UI_crea_sheet.Controls.Add($Label2)
$UI_crea_sheet.Controls.Add($CheckBox1)
$UI_crea_sheet.Controls.Add($Num_pag)
$UI_crea_sheet.Controls.Add($GroupBox1)
$UI_crea_sheet.Controls.Add($S_Collection)
$UI_crea_sheet.Controls.Add($Label1)
$UI_crea_sheet.Controls.Add($sheet_name)
$UI_crea_sheet.Controls.Add($Cancel_button)
$UI_crea_sheet.Controls.Add($create_button)
$UI_crea_sheet.Name = [System.String]'UI_crea_sheet'
$UI_crea_sheet.Text = [System.String]'RenomBrator'
$UI_crea_sheet.add_Load($Form1_Load)
$GroupBox1.ResumeLayout($false)
([System.ComponentModel.ISupportInitialize]$Num_pag).EndInit()
$UI_crea_sheet.ResumeLayout($false)
$UI_crea_sheet.PerformLayout()
Add-Member -InputObject $UI_crea_sheet -Name Vews_list -Value $Vews_list -MemberType NoteProperty
Add-Member -InputObject $UI_crea_sheet -Name create_button -Value $create_button -MemberType NoteProperty
Add-Member -InputObject $UI_crea_sheet -Name Cancel_button -Value $Cancel_button -MemberType NoteProperty
Add-Member -InputObject $UI_crea_sheet -Name sheet_name -Value $sheet_name -MemberType NoteProperty
Add-Member -InputObject $UI_crea_sheet -Name S_views -Value $S_views -MemberType NoteProperty
Add-Member -InputObject $UI_crea_sheet -Name Label1 -Value $Label1 -MemberType NoteProperty
Add-Member -InputObject $UI_crea_sheet -Name S_Collection -Value $S_Collection -MemberType NoteProperty
Add-Member -InputObject $UI_crea_sheet -Name GroupBox1 -Value $GroupBox1 -MemberType NoteProperty
Add-Member -InputObject $UI_crea_sheet -Name Num_pag -Value $Num_pag -MemberType NoteProperty
Add-Member -InputObject $UI_crea_sheet -Name CheckBox1 -Value $CheckBox1 -MemberType NoteProperty
Add-Member -InputObject $UI_crea_sheet -Name Label2 -Value $Label2 -MemberType NoteProperty
Add-Member -InputObject $UI_crea_sheet -Name S_Titlebolock -Value $S_Titlebolock -MemberType NoteProperty
Add-Member -InputObject $UI_crea_sheet -Name Label3 -Value $Label3 -MemberType NoteProperty
Add-Member -InputObject $UI_crea_sheet -Name S_Sheet_Title -Value $S_Sheet_Title -MemberType NoteProperty
Add-Member -InputObject $UI_crea_sheet -Name S_sheet_name -Value $S_sheet_name -MemberType NoteProperty
Add-Member -InputObject $UI_crea_sheet -Name TextBox1 -Value $TextBox1 -MemberType NoteProperty
}
. InitializeComponent
