/* Copyright 2014-2016 Sandia Corporation. Under the terms of Contract
 * DE-AC04-94AL85000, there is a non-exclusive license for use of this work
 * by or on behalf of the U.S. Government. Export of this program may require
 * a license from the United States Government.
 *
 * This file is part of the Power API Prototype software package. For license
 * information, see the LICENSE file in the top level directory of the
 * distribution.
*/
#include <stdio.h>
#include <sys/timeb.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>

#include <netdb.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <sys/socket.h>
#include <poll.h>
#include <sys/types.h>
#include <ctype.h>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>

#include "pwr_dev.h"
#include "util.h"
#include "redfish_dev.h"
#include <pwr/util.h>

#define ERR_NO -1
#define SUCCESS 0

typedef struct {
        char *attr_name;
        //void;
} pwr_redfish_attr;
#define PWR_DEV_ATTR(X) ((pwr_redfish_attr *)(X))

typedef struct {
    char *device_name;
    pwr_redfish_attr *attr; 
} pwr_redfish_device;
#define PWR_R_DEVICE(X) ((pwr_redfish_device *)(X))

typedef struct {
	/* define our data */
	char *entity;	
	char *host;
	char *port;
	char *node;
	int socket_fd;
} pwr_redfish_dev_t;
#define PWR_REDFISH_DEV(X) ((pwr_redfish_dev_t *)(X))

typedef struct {
    pwr_redfish_dev_t *dev;
    char *dev_name;
    int file_fd;
} pwr_redfish_fd_t;
#define PWR_REDFISH_FD(X) ((pwr_redfish_fd_t *)(X))


static plugin_devops_t devOps = {
    .open   = redfish_dev_open,
    .close  = redfish_dev_close,
    .read   = redfish_dev_read,
    .write  = redfish_dev_write,
    .readv  = redfish_dev_readv,
    .writev = redfish_dev_writev,
/*
    .time   = redfish_dev_time,
    .clear  = redfish_dev_clear,
    .log_start = redfish_dev_log_start,
    .log_stop = redfish_dev_log_stop,
    .get_samples = redfish_dev_get_samples,
*/
};


typedef struct {
        int fd, cfd;
        unsigned short local;
        char* agent_addr;
        unsigned short agent_port;

} redfish_context;
#define REDFISH_CNTX(X) ((redfish_context *)(X))



static plugin_devops_t* redfish_dev_init( const char *initstr )
{
    char *entity, *host, *node, *port;
    static int socket;
 	 	
    plugin_devops_t *dev = malloc( sizeof(devOps) );
    *dev = devOps;
     
     DBGP("initstr='%s'\n",initstr);
     //printf("initstr='%s'\n",initstr);

     if( parse(initstr, &entity, &host, &port, &node) != 0) {
	return (plugin_devops_t *)NULL;
     }	
     pwr_redfish_dev_t *p = malloc( sizeof(pwr_redfish_dev_t ) );
     bzero( p, sizeof(pwr_redfish_dev_t) );
	 p->entity = entity;
     p->host = host;
     p->port = port;
     p->node = node;
     dev->private_data = p; 
	
    return dev;

}


int parse(char *string, char **entity, char **host, char **port, char **node) {

	char *token;
	unsigned long int token_len; 
	if ( (token = strtok(string,":")) == NULL) {
		return ERR_NO;
	}
	token_len = strlen(token);
	*entity = malloc(token_len+1);
	bzero(*entity, token_len+1);
	strncpy(*entity, token, token_len);
	if ( (token = strtok(NULL,":")) == NULL) {
		return ERR_NO;
	}
	
	token_len = strlen(token);
	*host = malloc(token_len+1);
	bzero(*host,token_len+1);
	strncpy(*host, token, token_len); 
	if ( (token = strtok(NULL,":")) == NULL) {
		return ERR_NO;
	}	
	token_len = strlen(token);
	*port = malloc(token_len+1);
	bzero(*port, token_len+1);
	strncpy(*port, token, token_len);
	if ( (token = strtok(NULL,":")) == NULL) {
		return ERR_NO;
	}	
	token_len = strlen(token);
	*node = malloc(token_len+1);
	bzero(*node, token_len+1);
	strncpy(*node, token, token_len);
	return SUCCESS;


}	


int redfish_connect(pwr_redfish_dev_t *p) 
{
	int sockfd = 0;	
	int k;
        struct sockaddr_in serv_addr;
	struct addrinfo *res;
	int enable = 1;
	res = malloc(sizeof(struct addrinfo));
	bzero(res, sizeof(struct addrinfo));
	//printf("host = %s, port = %s\n", p->host, p->port); 
	if( (k = getaddrinfo(p->host, p->port, NULL, &res)) != 0) {
		perror("error:");
		return ERR_NO;
	}

        if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
                assert("socket creation failed\n");
		return ERR_NO;
        }

	if (connect(sockfd, res->ai_addr,res->ai_addrlen) < 0) {
     		 perror("connect :");
		 assert("Connection failed\n");	
		return ERR_NO;
   	}
	setsockopt( sockfd, SOL_TCP, TCP_NODELAY, (char *) &enable, sizeof(int) );
	p->socket_fd = sockfd;
	//printf("sckfd =%d \n", sockfd);
	//return SUCCESS;
	return sockfd;
}



static pwr_fd_t redfish_dev_open( plugin_devops_t* ops, const char *openstr )
{
    
    char string[200];

    pwr_redfish_fd_t *fd = malloc(sizeof(pwr_redfish_fd_t));	
    bzero( fd, sizeof(pwr_redfish_fd_t) );	
    	
    pwr_redfish_dev_t *p = (pwr_redfish_dev_t *) ops->private_data;
    PWR_REDFISH_FD(fd)->dev = p;
	PWR_REDFISH_FD(fd)->dev_name = (char *) malloc(strlen(openstr)+1);
	strcpy(PWR_REDFISH_FD(fd)->dev_name, openstr);
    
    DBGP("Device Name=%s\n", PWR_REDFISH_FD(fd)->dev_name);
    //printf("Device Name=%s\n", PWR_REDFISH_FD(fd)->dev_name);
	//printf("entity = %s, node = %s, host = %s, port = %s\n", p->entity, p->node, p->host, p->port);
    if((fd->file_fd = redfish_connect(p)) < 0) {
	//printf("Inside error condition\n");    
	return (plugin_devops_t *)NULL;
    }
    return fd;
}



static int redfish_dev_read( pwr_fd_t fd, PWR_AttrName type, void* ptr, unsigned int length, PWR_Time* ts )
{
	int ret = 0, len =0, size = 0;
	char string[200];
	char buf[200], *p ,*a;
	double d, now;
	struct timeval tv;
	
	char *entity = PWR_REDFISH_FD(fd)->dev->entity;
	char *node = PWR_REDFISH_FD(fd)->dev->node;
	char *dev_name = PWR_REDFISH_FD(fd)->dev_name;
	int file_fd = PWR_REDFISH_FD(fd)->file_fd;
	
	now = getTimeSec();
	p = buf;
	//pwr_redfish_fd_t *obj = (pwr_redfish_fd_t *)fd;

	a = attrNameToString(type);
	sprintf(string,"get:%s:%s:%s:%s;", entity, node, dev_name, a);
	//printf("path to be opened %s\n", string);
	if ((send(file_fd, string, strlen(string), NULL)) < 0) {
		perror("send:");
		//printf("Sending failed\n");
		return ERR_NO;
	}

	if ((recv(file_fd, p, 20, NULL)) < 0) {
		//printf("Error while reading\n");
		perror("recv :");
		return ERR_NO;
	}
	d = strtod(p,NULL);
	bcopy(&d, (double *)ptr, sizeof(double)); 
		
	return PWR_RET_SUCCESS;
	
}


static int redfish_dev_write( pwr_fd_t fd, PWR_AttrName type, void* ptr, unsigned int len )
{

	
	int file_fd;
	char string[200];
	char buf[200], *a;
	
	pwr_redfish_fd_t *obj = (pwr_redfish_fd_t *)fd;
	file_fd = obj->file_fd;

	a = attrNameToString(type);
	strcpy(ptr, "1234");
	sprintf(string,"set:ilo:%s:%s:%s:%s;", obj->dev->node, obj->dev_name, a, ptr);
	//printf("path to be opened %s\n", string);
	if ((send(file_fd, string, strlen(string), NULL)) < 0) {
		perror("send:");
		//printf("Sending failed\n");
		return ERR_NO;
	}

	//printf("path opened\n");
	if ((recv(file_fd, buf, 10, NULL)) < 0) {
		//printf("Error while receiving\n");
		perror("recv :");
		return ERR_NO;
	}
        //printf("Setting value done %s\n", buf);

	return PWR_RET_SUCCESS;
}


static int redfish_dev_readv( pwr_fd_t fd, unsigned int arraysize, const PWR_AttrName attrs[], void* buf,
                        PWR_Time ts[], int status[] )
{
        return PWR_RET_SUCCESS;
}


static int redfish_dev_writev( pwr_fd_t fd, unsigned int arraysize, const PWR_AttrName attrs[], void* ptr, int status[] )
{

        return PWR_RET_SUCCESS;    	

}



static int redfish_dev_close( pwr_fd_t fd )
{
    DBGP("\n");

    return 0;
}
static int redfish_dev_final( plugin_devops_t *ops )
{
    DBGP("\n");
    free(ops->private_data);
    return 0;
}

static plugin_dev_t dev = {
    .init   = redfish_dev_init, 
    .final  = redfish_dev_final,
};

plugin_dev_t* getDev() {
    return &dev;
}

static double getTime() {
    struct timeval tv;
    gettimeofday(&tv,NULL);
	double value; 
    value = tv.tv_sec * 1000000000;
    value += tv.tv_usec * 1000;
	return value;
}

static double getTimeSec()
{
	return getTime() / 1000000000.0;
}
  
