medium_query = """
    query ProfilePubHandlerQuery(
        $id: ID, 
        $username: ID, 
        $homepagePostsLimit: PaginationLimit, 
        $homepagePostsFrom: String, 
        $includeDistributedResponses: Boolean
    ) {
        userResult(id: $id, username: $username) {
            ... on User {
            id
            name
            ...ProfilePubScreen_user
            __typename
            }
        }
    }

    fragment ProfilePubScreen_user on User {
        id
        homepagePostsConnection(
            paging: { limit: $homepagePostsLimit, from: $homepagePostsFrom }, 
            includeDistributedResponses: $includeDistributedResponses
        ) {
            posts {
                id
                title
            }
        }
    }
"""
