/*
 * Copyright 2014-2016 Sandia Corporation. Under the terms of Contract
 * DE-AC04-94AL85000, there is a non-exclusive license for use of this work
 * by or on behalf of the U.S. Government. Export of this program may require
 * a license from the United States Government.
 *
 * This file is part of the Power API Prototype software package. For license
 * information, see the LICENSE file in the top level directory of the
 * distribution.
*/

#ifndef REDFISH_DEV_H
#define REDFISH_DEV_H

#include "pwrdev.h"

#ifdef __cplusplus
extern "C" {
#endif



static plugin_devops_t* redfish_dev_init( const char *initstr );
static pwr_fd_t redfish_dev_open( plugin_devops_t* ops, const char *openstr );
static int redfish_dev_read( pwr_fd_t fd, PWR_AttrName type, void* ptr, unsigned int len, PWR_Time* ts );
static int redfish_dev_write( pwr_fd_t fd, PWR_AttrName type, void* ptr, unsigned int len );
static int redfish_dev_readv( pwr_fd_t fd, unsigned int arraysize, const PWR_AttrName attrs[], void* buf, PWR_Time ts[], int status[] );
static int redfish_dev_writev( pwr_fd_t fd, unsigned int arraysize, const PWR_AttrName attrs[], void* ptr, int status[] );
static int redfish_dev_parse( const char *initstr, unsigned int *saddr, unsigned int *sport );
static int redfish_dev_close( pwr_fd_t fd );
static int redfish_dev_final( plugin_devops_t *ops );
static int redfish_dev_time(pwr_fd_t fd, PWR_Time *timestamp );
static int redfish_dev_clear(pwr_fd_t fd);
static int redfish_dev_log_start(pwr_fd_t fd, PWR_AttrName name);
static int redfish_dev_log_stop(pwr_fd_t fd, PWR_AttrName name);
static int redfish_dev_get_samples( pwr_fd_t fd, PWR_AttrName name, PWR_Time* ts, double period, unsigned int* nSamples, void* buf );

static double getTime();
static double getTimeSec();

#ifdef __cplusplus
}
#endif

#endif
