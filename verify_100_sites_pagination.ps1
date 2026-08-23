$base = "http://localhost:8000/api/v1/heritage-sites"

for ($page = 1; $page -le 10; $page++) {
    $response = Invoke-RestMethod `
        -Uri "${base}?page=${page}&page_size=10" `
        -Method GET

    Write-Host "PAGE $page : $($response.data.sites.Count) sites"
}
