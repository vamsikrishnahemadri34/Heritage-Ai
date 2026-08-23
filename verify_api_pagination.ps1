$base = "http://localhost:8000/api/v1/heritage-sites"

for ($page = 1; $page -le 5; $page++) {

    $url = $base + "?page=" + $page + "&page_size=20"

    $response = Invoke-RestMethod `
        -Uri $url `
        -Method GET

    Write-Host "PAGE $page : $($response.data.sites.Count) sites"
}
