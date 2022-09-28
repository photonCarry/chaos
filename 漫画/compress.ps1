Get-ChildItem .\ | ForEach-Object -Process{
    if($_ -is [System.IO.DirectoryInfo])
    {
        Write-Host("compress", $_.name);
        $compress = @{
            LiteralPath   = $_.name
            CompressionLevel = "Fastest"
            DestinationPath = ".\" + $_.name + ".zip"
        }
        Compress-Archive @compress
    }
}