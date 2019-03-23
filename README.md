# A few misc. tools for athena++

# reader.py

Relies on the script athena_read athena/vis/python/athena_read.py
    aread(filename) # chooses right athena_read reader based on filename suffix
    cyltocart(r,phi,z) # basic transformation
    sphtocary(r,theta,phi) #basic transformation
    data # output of athena_read or aread
    data_coord(data) # gets x1,x2,x3
    data_rho(data) # gets density
    data_phi(data) # gets gravitational potential
    parsedata(data) # tries to return x1,x2,x3,rho,press,v1,v2,v3,bcc1,bcc2,bcc3
    getfiles(suffix) # uses os to return all files with suffix as a list

# view_neighborhood.py

Some (not completely general) functions to help diagnose a simulation by looking at local problematic regions. 

    data # 3-D numpy array
    slice_neigh(data,indices,size) # grabs a local slice around indices
    view(data) # makes scatterplot of data
    view4(datas) # makes scatterplot with some direction
  				