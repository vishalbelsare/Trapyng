
from scipy.special import hyp1f1
from scipy.special import gamma
import numpy as np
import general_func as gf 

#def preprocess_input(X, clusters_relation):
#    """ 
#    This funciton preprocess the input so that we 
#
#    If it is "independent" then we just need X". 
#    
#    if it is 
#    """
#  if (clusters_relation == "independent"):
#        if (type(X) == type([])): # If we are given a list where each element is a matrix of data we just merge them
#                                  # We expect it to be filled with matrix (Nsam_i, Ndim_j)
#            X = np.concatenate(X, axis = 0)
#        N,D = X.shape   # Number of IDD samples
#        
#    elif (clusters_relation == "MarkovChain1"):
#        N = len(data)         # Number of Realizations of the HMM
#        D = data[0].shape[1]; # Dimensionality of samples
#    
#        ######## THIS IS A CONCATENATED VERSION OF THE SAMPLES THAT WE NEED
#        ## For some parts of the algorithm we need all the samples in a vector, for
#        # example when computing the weighted estimatoin with responsability vector rk. 
#        # We take into account different chains, so we also use data
#        X = data[0]
#        for n in range(1,N):
#            X = np.concatenate((X, data[n]), axis = 0)
#    
#    return X, data, N,D

def preprocess_data(data):
    if (type(data) == type([])): # If we are given a list where each element is a matrix of data we just merge them
                          # We expect it to be filled with matrix (Nsam_i, Ndim_j)
        if (len(data) == 1):
            X = data[0]
        else:
            X = np.concatenate(data, axis = 0)
    else:
        X = data
    return X
            
def init_model_params(K,model_theta = None):
    # Here we will initialize the mixing coefficients parameters of the mixture model
    # MIXING COEFICIENTS
    # We set the mixing coefficients with uniform discrete distribution, this
    # way, the a priori probability of any vector to belong to any component is
    # the same.
        
    if (type(model_theta) == type(None)): # If not given an initialization
        pimix = np.ones((1,K));
        pimix = pimix*(1/float(K));
    else:
        pi_init = model_theta[0]
        pimix = np.array(pi_init).reshape(1,K)
        
    return [pimix]

def get_model_theta(r):
    """
    This function computes the pimix 
    """
    N,K = r.shape
    pimix = np.zeros((1,K))
    for k in range(K):
        pimix[:,k] = np.sum(r[:,k])/N;
        model_theta = [pimix]
    return model_theta


def get_theta(X, r, distribution):
    """ This function aims to estimate the new theta values for all the clusters.
        For each cluster it will call the estimation function "distribution.theta_estimator(X, rk)".
        If it fails, it should create a RuntimeExeption, which is handled here by setting the parameters to None.
        This will be handled later.
    
    """
    # Cluster by Cluster it will estimate them, if it cannot, then it 
    
    # We only need the old mus for checking the change of sign
    # Maybe in the future get this out
    N,D = X.shape
    N,K = r.shape
    
    # Estimated theta
    theta = distribution.get_theta(X, r) # Parameters of the k-th cluster

    return theta

def get_samples_loglikelihood(X,theta,distribution):
    """
    This function simply computes the likelihood for each sample, to each of the
    clusters 
    """
    loglike = distribution.pdf_log_K(X,theta)
    N,K = loglike.shape
    D = theta[0][0].size
#    lw = 7
#    window = np.ones((lw,1))/float(lw)
#    for k in range(K):
#        loglike[:,k] = np.convolve(loglike[:,k].flatten(), window.flatten(), mode = "full")[:-(lw-1)]
        
#    loglike[:,:] =  loglike[:,:] * 10# + np.log(10000000000000000000)  # Increase twice the likelihood
#    samples_ll =  gf.sum_logs(loglike, byRow = True)
#        print samples_ll.shape
#    loglike = loglike - samples_ll
#    loglike[:,:] =  loglike[:,:] * 1000#


#    loglike[:,:] =  loglike[:,:]  / (float(D/10))
    return loglike
     
def get_r_and_ll(data,distribution,theta, model_theta, loglike = None):
    # Combined funciton to obtain the loglikelihood and r in one step
    
    X = preprocess_data(data)
    N, D = X.shape
    K = len(theta)
    pimix = model_theta[0]
                        
     # Compute the pdf for all samples and all clusters
    if (type(loglike) == type(None)):
        loglike = get_samples_loglikelihood(X,theta, distribution)
    else:
        loglike = loglike
    
    
    r_log= np.log(pimix) + loglike
    samples_ll =  gf.sum_logs(r_log, byRow = True)
    ll = np.sum(samples_ll)
    

#    if(0):
#        for i in range(N):  # For every sample
#        #TODO: Can this not be done without a for ?
#            ll += gf.sum_logs(r_log[i,:])  # Marginalize clusters and product of samples probabilities!!
#            # Normalize the probability of the sample being generated by the clusters
#            Marginal_xi_probability = gf.sum_logs(r_log[i,:])
#            r_log[i,:] = r_log[i,:]- Marginal_xi_probability
#    else:

#        print samples_ll.shape

    r =  get_responsibilities(X,distribution,theta, model_theta, loglike = loglike)
    ## COMPUTE Responsibilities !!

    return r, ll


def get_responsibilities(X,distribution,theta, model_theta, loglike = None):
    X = preprocess_data(X)
    N, D = X.shape
    K = len(theta)
    pimix = model_theta[0]
    
    if (type(loglike) == type(None)):
        loglike = get_samples_loglikelihood(X,theta, distribution)
    else:
        loglike = loglike
        
    
    
#    loglike[:,0] =  loglike[:,0] - np.log(5)
    
    r_log = np.log(pimix) + loglike
    
    samples_ll =  gf.sum_logs(r_log, byRow = True)
    r_log = r_log - samples_ll
    
    ## Turn into hard decision
    if (0):
        rmax = np.argmax(r_log, axis = 1)
        N,K = r_log.shape
        hard_r = np.zeros(r_log.shape)
        for i in range(N):
            hard_r[i,rmax[i]] = 1
        hard_r = hard_r + 1e-200
        r_log = np.log(hard_r)
    
    
    r = np.exp(r_log)
    return r

def get_loglikelihood(data,distribution,theta, model_theta,loglike = None):
    # Combined funciton to obtain the loglikelihood and r in one step
    # The shape of X is (N,D)
    
    X = preprocess_data(data)
    N, D = X.shape
    K = len(theta)
    r_log = np.zeros((N,K))
    
    pimix = model_theta[0]
    ll = 0
#    print pimix
     # Compute the pdf for all samples and all clusters
    if (type(loglike) == type(None)):
         loglike = get_samples_loglikelihood(X,theta, distribution)
    else:
        loglike = loglike
        
    r_log[:,:] = np.log(pimix[:,:]) + loglike
    samples_ll =  gf.sum_logs(r_log[:,:], byRow = True)
#        print samples_ll.shape
    ll = np.sum(samples_ll)
        
    return ll

def manage_clusters(X,r, distribution, model_theta, theta_new, theta_prev):
    
    """ This function will deal with the generated clusters, 
    both from the estimation and the parameters.  
    For every cluster it will check if the estimation degenerated, if it did then
    we use the handler function to set the new ones. If it is None, then they will be removed.
    
    Then we check that the pdf of the distribution can be computed, a.k.a the normalization
    constant can be computed. If it cannot be computed then we call the handler. If the result is None,
    then the cluster will be removed !! """
    
    ## We avoid 0s in pimix...
    pimix = model_theta[0]
    pimix = pimix + 1e-200; pimix = pimix / np.sum(pimix)
    model_theta = [pimix]
    K = len(theta_new)
    Nsam,D = X.shape
    
    clusters_change = 0  # Flag is we modify the clusters so that we dont stop
                        # due to a decrease in likelihood.
                        
    theta_new, clusters_change = distribution.manage_clusters(X, r, theta_prev, theta_new)
                    
    ################## Last processing that you would like to do with everything ##############
    if  hasattr(distribution, 'use_chageOfClusters'):
        if (type(distribution.use_chageOfClusters) != type(None)):
            theta_new = distribution.use_chageOfClusters(theta_new, theta_prev)
    
    ############## Remove those clusters that are set to None ###################
    for k in range(K):
        k_inv = K - 1 -k
        if(type(theta_new[k_inv]) == type(None)):  # Degenerated cluster during estimation
            # Remove cluster from parameters
            theta_new,model_theta = remove_cluster(theta_new,pimix,k_inv)
            # Remove cluster from distribution data structure
            distribution.remove_cluster(k_inv)  
    
    return theta_new,model_theta, clusters_change


def remove_cluster(theta, model_theta, k):
    # This function removed the cluster k from the parameters
    theta.pop(k)
    pi = model_theta[0]
    pi = np.delete(pi, k, axis = 1)
    pi = pi / np.sum(pi)
    print ("$ Cluster %i removed" % (k))
    model_theta = [pi]
    return theta, model_theta





